import copy
import pandas as pd

from fuel_contour.model import SimulationInputs, simulate_plan
from conftest import set_plan


def test_physical_45_day_reserve_passes_at_start_of_2035(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    required = 100 * 45 / 365
    r = simulate_plan(
        demand, sources, config, blank_plan, blank_investments, blank_reserve,
        SimulationInputs(initial_inventory_t=required, initial_inventory_source="prestart purchase", initial_inventory_cost_m=100),
    )
    y = r.annual.set_index("year").loc[2035]
    assert y["physical_reserve_ok"]


def test_contractual_reserve_requires_bridge_coverage(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    required = 100 * 45 / 365
    p = set_plan(blank_plan, 2035, "E", required, 0, role="insurance")
    r0 = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    assert not r0.annual.set_index("year").loc[2035, "contractual_reserve_ok"]
    evidence = blank_reserve.copy()
    evidence["bridge_coverage_t"] = evidence["bridge_coverage_t"].astype(float)
    evidence.loc[evidence["year"] == 2035, "bridge_coverage_t"] = 100 * 42 / 365
    r1 = simulate_plan(demand, sources, config, p, blank_investments, evidence, SimulationInputs())
    assert r1.annual.set_index("year").loc[2035, "contractual_reserve_ok"]


def test_model_accepts_added_source_and_future_period_via_data_and_config(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    demand2 = pd.concat([demand, pd.DataFrame([{
        "year": 2041, "base_total_t": 430, "base_critical_t": 270, "low_total_t": 344, "high_total_t": 537.5
    }])], ignore_index=True)
    source_f = sources.iloc[0].copy()
    source_f["source_id"] = "F"
    source_f["name"] = "Research-Source-F"
    source_f["max_capacity_tpy"] = 50
    source_f["variable_cost_m_per_t"] = 10
    source_f["reservation_fee_m_per_tpy"] = 0
    source_f["take_or_pay_share"] = 0
    source_f["available_from"] = 2041
    sources2 = pd.concat([sources, pd.DataFrame([source_f])], ignore_index=True)
    config2 = copy.deepcopy(config)
    config2["horizon"] = config["horizon"] + [2041]
    plan2 = pd.concat([blank_plan, pd.DataFrame([{
        "year": 2041, "source_id": sid, "reserved_capacity_tpy": 0, "planned_gross_delivery_t": 0, "role": "base"
    } for sid in sources2["source_id"]])], ignore_index=True)
    inv2 = pd.concat([blank_investments, pd.DataFrame([{
        "year": 2041, "zbo_capex_m": 0, "isru_capex_m": 0, "earth_new_option_fee_m": 0, "earth_new_exercise_capex_m": 0
    }])], ignore_index=True)
    reserve2 = pd.concat([blank_reserve, pd.DataFrame([{
        "year": 2041, "physical_start_inventory_target_t": 0, "emergency_reserved_t": 0, "bridge_coverage_t": 0, "note": "research extension"
    }])], ignore_index=True)
    r = simulate_plan(demand2, sources2, config2, plan2, inv2, reserve2, SimulationInputs())
    assert 2041 in r.annual["year"].tolist()
    assert "F" in r.source_costs["source_id"].tolist()


def test_added_source_respects_available_from(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    f = sources.iloc[0].copy()
    f["source_id"] = "F"
    f["name"] = "Research-Source-F"
    f["available_from"] = 2038
    sources2 = pd.concat([sources, pd.DataFrame([f])], ignore_index=True)
    p = pd.concat([blank_plan, pd.DataFrame([{
        "year": 2037, "source_id": "F", "reserved_capacity_tpy": 10.0,
        "planned_gross_delivery_t": 10.0, "first_delivery_month": 1,
        "order_date": "2035-01-01", "role": "research"
    }])], ignore_index=True)
    r = simulate_plan(demand, sources2, config, p, blank_investments, blank_reserve, SimulationInputs())
    c = r.constraints.query("constraint == 'source_availability' and year == 2037")
    assert not c.empty
