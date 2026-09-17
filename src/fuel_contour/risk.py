from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from .model import SimulationResult


@dataclass
class MonteCarloResult:
    summary: pd.DataFrame
    trials: pd.DataFrame
    assumptions: dict[str, Any]


def _reliability_for(source: pd.Series, year: int, first_active_year: int | None) -> float:
    sid = str(source["source_id"])
    if sid == "C" and first_active_year is not None:
        if year == first_active_year:
            return float(source.get("reliability_first_operating_year", 0.88))
        if year > first_active_year:
            return float(source.get("reliability_later", 0.94))
    col = f"case_reliability_{year}"
    value = source.get(col, np.nan)
    if pd.isna(value):
        return 1.0
    return float(value)


def monte_carlo_channel_availability(
    deterministic: SimulationResult,
    sources: pd.DataFrame,
    n_trials: int = 5000,
    seed: int = 2035,
    common_earth_outage_probability: float = 0.0,
) -> MonteCarloResult:
    """Optional research screen, separate from the case control calculation.

    Mathematical interpretation used here:
    - each case reliability coefficient is interpreted as the annual probability that a
      source remains available for its full planned delivery in that year;
    - source-year events are independent unless ``common_earth_outage_probability`` is
      explicitly set above zero;
    - a common Earth outage disables A/B/C/E for that year;
    - the deterministic plan's planned/scenario-adjusted gross quantities and storage
      mode are otherwise unchanged.

    This is not an empirical forecast. It is one reproducible way to expose the
    consequences of a chosen interpretation of the case reliability coefficients.
    """
    if n_trials < 100:
        raise ValueError("n_trials must be at least 100 for a meaningful numerical screen")
    if not (0.0 <= common_earth_outage_probability <= 1.0):
        raise ValueError("common_earth_outage_probability must be in [0,1]")

    rng = np.random.default_rng(seed)
    src = sources.set_index("source_id", drop=False)
    sc = deterministic.source_costs.copy()
    years = sorted(deterministic.annual["year"].astype(int).unique())
    sids = list(src.index.astype(str))

    first_active_c = deterministic.investment_status.get("earth_new_active_year")
    availability = np.ones((n_trials, len(years), len(sids)), dtype=float)
    for yi, year in enumerate(years):
        common_fail = rng.random(n_trials) < common_earth_outage_probability
        for si, sid in enumerate(sids):
            rel = _reliability_for(src.loc[sid], year, first_active_c)
            own_ok = rng.random(n_trials) < rel
            if sid in {"A", "B", "C", "E"} and common_earth_outage_probability > 0:
                own_ok = own_ok & (~common_fail)
            availability[:, yi, si] = own_ok.astype(float)

    start_inventory = np.full(n_trials, float(deterministic.annual.iloc[0]["start_inventory_t"]), dtype=float)
    shortage_by_year = np.zeros((n_trials, len(years)), dtype=float)
    critical_shortage_by_year = np.zeros((n_trials, len(years)), dtype=float)
    total_demand_by_year = deterministic.annual.set_index("year").loc[years, "total_demand_t"].to_numpy(dtype=float)
    critical_demand_by_year = deterministic.annual.set_index("year").loc[years, "critical_demand_t"].to_numpy(dtype=float)
    served_by_year = np.zeros_like(shortage_by_year)
    critical_served_by_year = np.zeros_like(shortage_by_year)

    for yi, year in enumerate(years):
        annual_row = deterministic.annual[deterministic.annual["year"] == year].iloc[0]
        capacity = float(annual_row["storage_capacity_t"])
        loss_rate = float(annual_row["loss_rate"])
        month_rows = deterministic.monthly[deterministic.monthly["year"] == year].sort_values("month")
        source_annual = sc[sc["year"] == year].set_index("source_id")

        for _, mrow in month_rows.iterrows():
            weight = float(mrow["days"]) / 365.0
            gross = np.zeros(n_trials, dtype=float)
            for si, sid in enumerate(sids):
                planned_actual = float(source_annual.loc[sid, "actual_gross_delivery_t"]) if sid in source_annual.index else 0.0
                gross += planned_actual * weight * availability[:, yi, si]
            net = gross * (1.0 - loss_rate)
            before = np.minimum(start_inventory + net, capacity)
            crit_d = float(critical_demand_by_year[yi]) * weight
            tot_d = float(total_demand_by_year[yi]) * weight
            noncrit_d = max(tot_d - crit_d, 0.0)
            crit_served = np.minimum(before, crit_d)
            after_crit = before - crit_served
            noncrit_served = np.minimum(after_crit, noncrit_d)
            total_served = crit_served + noncrit_served
            start_inventory = np.maximum(before - total_served, 0.0)
            served_by_year[:, yi] += total_served
            critical_served_by_year[:, yi] += crit_served

        shortage_by_year[:, yi] = total_demand_by_year[yi] - served_by_year[:, yi]
        critical_shortage_by_year[:, yi] = critical_demand_by_year[yi] - critical_served_by_year[:, yi]

    total_service = served_by_year / total_demand_by_year[None, :]
    critical_service = critical_served_by_year / critical_demand_by_year[None, :]
    target_total = 0.97
    target_critical = 0.99

    summary_rows: list[dict[str, Any]] = []
    for yi, year in enumerate(years):
        summary_rows.append({
            "year": year,
            "mean_total_service": float(total_service[:, yi].mean()),
            "p05_total_service": float(np.quantile(total_service[:, yi], 0.05)),
            "prob_total_below_97pct": float((total_service[:, yi] < target_total).mean()),
            "mean_critical_service": float(critical_service[:, yi].mean()),
            "p05_critical_service": float(np.quantile(critical_service[:, yi], 0.05)),
            "prob_critical_below_99pct": float((critical_service[:, yi] < target_critical).mean()),
            "mean_shortage_t": float(shortage_by_year[:, yi].mean()),
            "p95_shortage_t": float(np.quantile(shortage_by_year[:, yi], 0.95)),
        })

    total_shortage = shortage_by_year.sum(axis=1)
    trials = pd.DataFrame({
        "trial": np.arange(n_trials, dtype=int),
        "total_shortage_t": total_shortage,
        "min_total_service": total_service.min(axis=1),
        "min_critical_service": critical_service.min(axis=1),
    })
    assumptions = {
        "n_trials": int(n_trials),
        "seed": int(seed),
        "reliability_interpretation": "annual Bernoulli full-channel availability",
        "source_year_independence": common_earth_outage_probability == 0.0,
        "common_earth_outage_probability": float(common_earth_outage_probability),
        "control_calculation_modified": False,
        "warning": "This is a research scenario, not an empirical probability forecast.",
    }
    return MonteCarloResult(summary=pd.DataFrame(summary_rows), trials=trials, assumptions=assumptions)
