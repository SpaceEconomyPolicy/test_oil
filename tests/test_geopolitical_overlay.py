import pytest

from fuel_contour.model import SimulationInputs, simulate_plan
from conftest import set_plan


def test_research_price_overlay_changes_only_selected_year(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2038, "A", 100, 100)
    p["order_date"] = p["order_date"].fillna("").astype(str)
    p.loc[(p.year == 2038) & (p.source_id == "A"), "order_date"] = "2036-12-31"
    base = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    shock = simulate_plan(
        demand, sources, config, p, blank_investments, blank_reserve,
        SimulationInputs(research_variable_price_multipliers={"A": {"2038": 1.3}}),
    )
    base_price = base.source_costs.query("year == 2038 and source_id == 'A'").iloc[0].variable_price_m_per_t
    shock_price = shock.source_costs.query("year == 2038 and source_id == 'A'").iloc[0].variable_price_m_per_t
    assert shock_price == pytest.approx(base_price * 1.3)
    a2039 = shock.source_costs.query("year == 2039 and source_id == 'A'").iloc[0]
    assert a2039.variable_price_m_per_t == pytest.approx(6.2)
