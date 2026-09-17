"""Run a small deterministic control calculation without the web UI."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fuel_contour.io import load_case, load_investments, load_plan, load_reserve_evidence
from fuel_contour.model import SimulationInputs, simulate_plan


demand, sources, config = load_case(ROOT)
plan = load_plan(ROOT / "data" / "blank_plan.csv")
investments = load_investments(ROOT / "data" / "investment_schedule_blank.csv")
reserve = load_reserve_evidence(ROOT / "data" / "reserve_evidence_blank.csv")
result = simulate_plan(demand, sources, config, plan, investments, reserve, SimulationInputs())
print(result.annual[["year", "total_demand_t", "total_served_t", "total_shortage_t"]].to_string(index=False))
print("hard constraints ok:", result.feasible_hard_constraints)
print("expected for blank starter: False")
