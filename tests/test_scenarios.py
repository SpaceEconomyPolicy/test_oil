from fuel_contour.scenarios import demand_for_scenario, delivery_factor, variable_price


def test_standard_demand_is_exact_case_series(case):
    demand, sources, config = case
    d = demand_for_scenario(demand, "standard", config)
    assert d["total_demand_t"].tolist() == [100.0, 140.0, 190.0, 250.0, 320.0, 390.0]
    assert d["critical_demand_t"].tolist() == [80.0, 105.0, 135.0, 170.0, 210.0, 250.0]


def test_stress_changes_only_specified_demand_years(case):
    demand, _, config = case
    d = demand_for_scenario(demand, "mandatory_stress", config).set_index("year")
    assert d.loc[2037, "total_demand_t"] == 190.0
    assert d.loc[2038, "total_demand_t"] == 287.5
    assert d.loc[2040, "critical_demand_t"] == 287.5


def test_low_high_keep_base_critical_share(case):
    demand, _, config = case
    low = demand_for_scenario(demand, "low_demand", config).set_index("year")
    high = demand_for_scenario(demand, "high_demand", config).set_index("year")
    base_share = 170 / 250
    assert abs(low.loc[2038, "critical_demand_t"] / low.loc[2038, "total_demand_t"] - base_share) < 1e-12
    assert abs(high.loc[2038, "critical_demand_t"] / high.loc[2038, "total_demand_t"] - base_share) < 1e-12


def test_mandatory_stress_price_and_isru_delivery_factor(case):
    _, sources, config = case
    s = sources.set_index("source_id")
    assert variable_price(s.loc["A"], 2038, "mandatory_stress", config) == 6.2 * 1.25
    assert variable_price(s.loc["A"], 2040, "mandatory_stress", config) == 6.2
    assert variable_price(s.loc["C"], 2038, "mandatory_stress", config) == 7.1
    assert delivery_factor("D", 2038, "mandatory_stress", config) == 0.55
    assert delivery_factor("D", 2039, "mandatory_stress", config) == 0.75
    assert delivery_factor("D", 2040, "mandatory_stress", config) == 1.0
