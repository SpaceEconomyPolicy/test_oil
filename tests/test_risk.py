from fuel_contour.model import SimulationInputs, simulate_plan
from fuel_contour.risk import monte_carlo_channel_availability
from conftest import set_plan


def test_monte_carlo_is_reproducible_with_seed(case, blank_plan, blank_investments, blank_reserve):
    demand, sources, config = case
    p = set_plan(blank_plan, 2035, "A", 100, 100)
    r = simulate_plan(demand, sources, config, p, blank_investments, blank_reserve, SimulationInputs())
    a = monte_carlo_channel_availability(r, sources, n_trials=200, seed=42)
    b = monte_carlo_channel_availability(r, sources, n_trials=200, seed=42)
    assert a.trials.equals(b.trials)
    assert a.assumptions["control_calculation_modified"] is False
