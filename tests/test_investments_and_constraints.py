import pytest
from fuel_contour.model import SimulationInputs, derive_investment_status, simulate_plan
from conftest import set_plan


def _set_inv(inv, year, **values):
    x = inv.copy()
    mask = x["year"] == year
    for key, value in values.items():
        x.loc[mask, key] = value
    return x


def test_earth_new_option_is_90_plus_270_not_720(case, blank_investments):
    _, _, config = case
    inv = _set_inv(blank_investments, 2035, earth_new_option_fee_m=90)
    inv = _set_inv(inv, 2036, earth_new_exercise_capex_m=270)
    status = derive_investment_status(inv, config, 730)
    assert status["earth_new_option_fee_total_m"] == 90
    assert status["earth_new_exercise_capex_total_m"] == 270
    assert status["earth_new_active_year"] == 2038


def test_isru_requires_full_funding_by_end_2037(case, blank_investments):
    _, _, config = case
    inv = _set_inv(blank_investments, 2037, isru_capex_m=1249)
    status = derive_investment_status(inv, config, 730)
    assert not status["isru_funded"]
    inv = _set_inv(blank_investments, 2037, isru_capex_m=1250)
    status = derive_investment_status(inv, config, 730)
    assert status["isru_funded"] and status["isru_active_year"] == 2038


def test_stress_does_not_multiply_isru_by_reliability(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    inv = _set_inv(blank_investments, 2037, isru_capex_m=1250)
    p = set_plan(blank_plan, 2038, "D", 100, 100)
    r = simulate_plan(demand, sources, config, p, inv, blank_reserve, SimulationInputs(scenario="mandatory_stress"))
    d = r.source_costs.query("year == 2038 and source_id == 'D'").iloc[0]
    assert d["actual_gross_delivery_t"] == pytest.approx(55.0)
    assert d["actual_gross_delivery_t"] != 55.0 * 0.78


def test_stress_loss_ceiling_is_checked_not_clamped(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    r = simulate_plan(demand, sources, config, blank_plan, blank_investments, blank_reserve, SimulationInputs(scenario="mandatory_stress"))
    y = r.annual.set_index("year").loc[2038]
    assert y["loss_rate"] == 0.045
    c = r.constraints.query("constraint == 'stress_storage_loss_rate' and year == 2038")
    assert len(c) == 1 and not bool(c.iloc[0]["ok"])


def test_zbo_case_coefficient_activates_only_after_full_capex(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    inv = _set_inv(blank_investments, 2036, zbo_capex_m=180)
    r = simulate_plan(demand, sources, config, blank_plan, inv, blank_reserve, SimulationInputs())
    assert r.annual.set_index("year").loc[2035, "loss_rate"] == 0.045
    assert r.annual.set_index("year").loc[2036, "loss_rate"] == 0.012
    assert r.annual.set_index("year").loc[2036, "storage_capacity_t"] == 120.0


def test_capex_limit_is_enforced(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    inv = _set_inv(blank_investments, 2037, isru_capex_m=1250, zbo_capex_m=180, earth_new_option_fee_m=90, earth_new_exercise_capex_m=300)
    r = simulate_plan(demand, sources, config, blank_plan, inv, blank_reserve, SimulationInputs())
    c = r.constraints.query("constraint == 'capex_through_2037'")
    assert len(c) == 1 and not bool(c.iloc[0]["ok"])


def test_emergency_base_use_more_than_two_consecutive_years_is_rejected(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = blank_plan.copy()
    for year in [2035, 2036, 2037]:
        p = set_plan(p, year, "E", 20, 10, role="base")
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    c = r.constraints[r.constraints["constraint"] == "emergency_base_use_consecutive_years"]
    assert not c.empty
