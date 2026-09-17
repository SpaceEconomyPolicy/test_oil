from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def project_root(start: str | Path | None = None) -> Path:
    if start is None:
        return Path(__file__).resolve().parents[2]
    return Path(start).resolve()


def load_case(root: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    root_path = project_root(root)
    demand = pd.read_csv(root_path / "data" / "demand.csv")
    sources = pd.read_csv(root_path / "data" / "sources.csv")
    with open(root_path / "configs" / "case_config.json", encoding="utf-8") as f:
        config = json.load(f)
    return demand, sources, config


def load_plan(path: str | Path) -> pd.DataFrame:
    plan = pd.read_csv(path)
    required = {"year", "source_id", "reserved_capacity_tpy", "planned_gross_delivery_t", "role"}
    missing = required.difference(plan.columns)
    if missing:
        raise ValueError(f"Plan is missing required columns: {sorted(missing)}")
    return plan


def load_investments(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "year",
        "zbo_capex_m",
        "isru_capex_m",
        "earth_new_option_fee_m",
        "earth_new_exercise_capex_m",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Investment schedule is missing required columns: {sorted(missing)}")
    return df


def load_reserve_evidence(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "year",
        "physical_start_inventory_target_t",
        "emergency_reserved_t",
        "bridge_coverage_t",
        "note",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Reserve evidence is missing required columns: {sorted(missing)}")
    return df
