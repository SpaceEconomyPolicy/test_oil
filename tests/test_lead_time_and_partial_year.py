import pandas as pd
import pytest

from fuel_contour.model import SimulationInputs, simulate_plan
from fuel_contour.scenarios import variable_price
from conftest import set_plan


def _with_order(plan, year, sid, order_date, first_month=1):
    p = plan.copy()
    if "order_date" in p.columns:
        p["order_date"] = p["order_date"].fillna("").astype(str)
    if "first_delivery_month" not in p.columns:
        p["first_delivery_month"] = 1
    if "order_date" not in p.columns:
        p["order_date"] = ""
    mask = (p["year"] == year) & (p["source_id"] == sid)
    p.loc[mask, "order_date"] = order_date
    p.loc[mask, "first_delivery_month"] = first_month
    return p


def test_lead_time_missing_is_reported_for_used_source(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "B", 20, 20)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    c = r.constraints.query("constraint == 'lead_time' and year == 2035")
    assert not c.empty
    assert not bool(c.iloc[0]["ok"])


def test_pre_horizon_order_satisfies_fixed_lead(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "B", 20, 20)
    p = _with_order(p, 2035, "B", "2034-08-01", 1)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    c = r.constraints.query("constraint == 'lead_time' and year == 2035")
    assert c.empty


def test_partial_year_reservation_payment_and_top(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "A", 100, 10)
    p = _with_order(p, 2035, "A", "2033-12-01", 7)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    row = r.source_costs.query("year == 2035 and source_id == 'A'").iloc[0]
    fraction = sum([31,31,30,31,30,31]) / 365.0  # Jul-Dec
    assert row["contract_period_fraction"] == pytest.approx(fraction)
    expected_paid = max(10, 0.70 * 100 * fraction)
    assert row["paid_quantity_t"] == pytest.approx(expected_paid)
    assert row["reservation_payment_m"] == pytest.approx(0.45 * 100 * fraction)
