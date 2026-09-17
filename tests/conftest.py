from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from fuel_contour.io import load_case, load_investments, load_plan, load_reserve_evidence


@pytest.fixture()
def root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture()
def case(root):
    return load_case(root)


@pytest.fixture()
def blank_plan(root):
    return load_plan(root / "data" / "blank_plan.csv")


@pytest.fixture()
def blank_investments(root):
    return load_investments(root / "data" / "investment_schedule_blank.csv")


@pytest.fixture()
def blank_reserve(root):
    return load_reserve_evidence(root / "data" / "reserve_evidence_blank.csv")


def set_plan(plan: pd.DataFrame, year: int, sid: str, reserved: float, delivery: float, role: str = "base") -> pd.DataFrame:
    p = plan.copy()
    p["reserved_capacity_tpy"] = p["reserved_capacity_tpy"].astype(float)
    p["planned_gross_delivery_t"] = p["planned_gross_delivery_t"].astype(float)
    mask = (p["year"] == year) & (p["source_id"] == sid)
    p.loc[mask, "reserved_capacity_tpy"] = reserved
    p.loc[mask, "planned_gross_delivery_t"] = delivery
    p.loc[mask, "role"] = role
    return p
