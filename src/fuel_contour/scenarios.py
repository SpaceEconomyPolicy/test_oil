from __future__ import annotations

from copy import deepcopy
from typing import Any

import pandas as pd


SCENARIOS = {"standard", "mandatory_stress", "low_demand", "high_demand"}


def demand_for_scenario(demand: pd.DataFrame, scenario: str, config: dict[str, Any]) -> pd.DataFrame:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    df = demand.copy()
    if scenario == "standard":
        df["total_demand_t"] = df["base_total_t"].astype(float)
        df["critical_demand_t"] = df["base_critical_t"].astype(float)
    elif scenario in {"low_demand", "high_demand"}:
        col = "low_total_t" if scenario == "low_demand" else "high_total_t"
        ratio = df["base_critical_t"] / df["base_total_t"]
        df["total_demand_t"] = df[col].astype(float)
        df["critical_demand_t"] = df["total_demand_t"] * ratio
    else:
        df["total_demand_t"] = df["base_total_t"].astype(float)
        df["critical_demand_t"] = df["base_critical_t"].astype(float)
        for year_str, multiplier in config["stress"]["demand_multiplier"].items():
            mask = df["year"].astype(int) == int(year_str)
            df.loc[mask, "total_demand_t"] *= float(multiplier)
            df.loc[mask, "critical_demand_t"] *= float(multiplier)
    return df[["year", "total_demand_t", "critical_demand_t"]]


def variable_price(source_row: pd.Series, year: int, scenario: str, config: dict[str, Any]) -> float:
    base = float(source_row["variable_cost_m_per_t"])
    if scenario != "mandatory_stress":
        return base
    source_id = str(source_row.get("source_id", source_row.name))
    multipliers = config["stress"].get("variable_price_multiplier", {}).get(source_id, {})
    return base * float(multipliers.get(str(year), 1.0))


def delivery_factor(source_id: str, year: int, scenario: str, config: dict[str, Any]) -> float:
    if scenario == "mandatory_stress" and source_id == "D":
        return float(config["stress"]["isru_delivery_factor"].get(str(year), 1.0))
    return 1.0


def scenario_metadata(scenario: str, config: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"scenario": scenario}
    if scenario == "mandatory_stress":
        out["service_is_hard_constraint"] = not bool(
            config["stress"].get("service_levels_are_targets_not_hard_constraints", True)
        )
        out["storage_loss_rate_ceiling_from_2038"] = float(
            config["stress"]["max_storage_loss_rate_from_2038"]
        )
    else:
        out["service_is_hard_constraint"] = scenario == "standard"
    return deepcopy(out)
