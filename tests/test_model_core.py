import pandas as pd

from fuel_contour.model import SimulationInputs, simulate_plan
from conftest import set_plan


def test_control_year_is_365_days_even_in_2036_and_2040(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    r = simulate_plan(demand, sources, config, blank_plan, blank_investments, blank_reserve, SimulationInputs())
    assert r.annual.set_index("year").loc[2036, "total_demand_t"] == 140.0
    assert r.annual.set_index("year").loc[2040, "total_demand_t"] == 390.0


def test_reliability_is_not_multiplied_into_standard_delivery(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "A", 100, 100)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    a = r.source_costs.query("year == 2035 and source_id == 'A'").iloc[0]
    assert a["actual_gross_delivery_t"] == 100.0
    assert a["actual_gross_delivery_t"] != 96.0


def test_losses_are_applied_once_to_gross_inbound(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "A", 100, 100)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    y = r.annual.set_index("year").loc[2035]
    assert abs(y["case_loss_t"] - 4.5) < 1e-9
    assert y["end_inventory_t"] >= 0
    assert y["total_shortage_t"] >= 0


def test_take_or_pay_uses_max_of_order_and_minimum_commitment(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "A", 100, 10)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    a = r.source_costs.query("year == 2035 and source_id == 'A'").iloc[0]
    assert a["paid_quantity_t"] == 70.0
    assert abs(a["variable_payment_m"] - 70.0 * 6.2) < 1e-9
    assert abs(a["reservation_payment_m"] - 100.0 * 0.45) < 1e-9


def test_negative_inventory_is_never_reported(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    r = simulate_plan(demand, sources, config, blank_plan, blank_investments, blank_reserve, SimulationInputs())
    assert (r.monthly["end_inventory_t"] >= 0).all()
    assert (r.monthly["total_shortage_t"] >= 0).all()


def test_initial_inventory_requires_source_and_financing(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    try:
        simulate_plan(demand, sources, config, blank_plan, blank_investments, blank_reserve, SimulationInputs(initial_inventory_t=10))
    except ValueError as exc:
        assert "explicit source" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_storage_overflow_is_numeric_violation(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "A", 190, 190)
    # huge initial inventory makes the first month exceed 70 t before demand
    r = simulate_plan(
        demand, sources, config, p, blank_investments, blank_reserve,
        SimulationInputs(initial_inventory_t=69, initial_inventory_source="prestart A", initial_inventory_cost_m=500),
    )
    assert r.annual.set_index("year").loc[2035, "capacity_overflow_t"] > 0
    c = r.constraints[r.constraints["constraint"] == "storage_capacity"]
    assert not c.empty and (~c["ok"]).all()
