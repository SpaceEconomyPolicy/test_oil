from __future__ import annotations

import json
from io import BytesIO
from typing import Any

import pandas as pd

from .model import SimulationResult


def result_to_excel(
    result: SimulationResult,
    plan: pd.DataFrame,
    investments: pd.DataFrame,
    metadata: dict[str, Any] | None = None,
    demand: pd.DataFrame | None = None,
    sources: pd.DataFrame | None = None,
    reserve_evidence: pd.DataFrame | None = None,
) -> bytes:
    """Create a reproducible workbook snapshot.

    The workbook is an export, not the computational core. It deliberately includes
    both outputs and the inputs that produced them so a jury member can trace a
    number back to the submitted plan.
    """
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        result.annual.to_excel(writer, sheet_name="annual", index=False)
        result.source_costs.to_excel(writer, sheet_name="source_costs", index=False)
        result.constraints.to_excel(writer, sheet_name="constraints", index=False)
        result.monthly.to_excel(writer, sheet_name="monthly", index=False)
        plan.to_excel(writer, sheet_name="plan_input", index=False)
        investments.to_excel(writer, sheet_name="investments", index=False)
        if reserve_evidence is not None:
            reserve_evidence.to_excel(writer, sheet_name="reserve_evidence", index=False)
        if demand is not None:
            demand.to_excel(writer, sheet_name="demand_input", index=False)
        if sources is not None:
            sources.to_excel(writer, sheet_name="sources_input", index=False)
        pd.DataFrame([result.metrics]).to_excel(writer, sheet_name="metrics", index=False)
        pd.DataFrame([result.investment_status]).to_excel(writer, sheet_name="investment_status", index=False)
        if result.warnings:
            pd.DataFrame({"warning": result.warnings}).to_excel(writer, sheet_name="warnings", index=False)
        if metadata:
            pd.DataFrame([metadata]).to_excel(writer, sheet_name="metadata", index=False)
    return buf.getvalue()


def project_bundle_json(
    plan: pd.DataFrame,
    investments: pd.DataFrame,
    reserve_evidence: pd.DataFrame,
    demand: pd.DataFrame,
    sources: pd.DataFrame,
    settings: dict[str, Any],
) -> str:
    """Save a complete editable project snapshot as JSON."""
    payload = {
        "version": 2,
        "plan": plan.where(pd.notna(plan), None).to_dict(orient="records"),
        "investments": investments.where(pd.notna(investments), None).to_dict(orient="records"),
        "reserve_evidence": reserve_evidence.where(pd.notna(reserve_evidence), None).to_dict(orient="records"),
        "demand": demand.where(pd.notna(demand), None).to_dict(orient="records"),
        "sources": sources.where(pd.notna(sources), None).to_dict(orient="records"),
        "settings": settings,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def load_project_bundle_json(text: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    payload = json.loads(text)
    if int(payload.get("version", 0)) != 2:
        raise ValueError("Unsupported project bundle version; expected version 2")
    return (
        pd.DataFrame(payload["plan"]),
        pd.DataFrame(payload["investments"]),
        pd.DataFrame(payload["reserve_evidence"]),
        pd.DataFrame(payload["demand"]),
        pd.DataFrame(payload["sources"]),
        dict(payload.get("settings", {})),
    )


# Compatibility helpers retained for notebooks/tests that may rely on the earlier mini-bundle.
def plan_bundle_json(plan: pd.DataFrame, investments: pd.DataFrame, settings: dict[str, Any]) -> str:
    payload = {
        "version": 1,
        "plan": plan.where(pd.notna(plan), None).to_dict(orient="records"),
        "investments": investments.where(pd.notna(investments), None).to_dict(orient="records"),
        "settings": settings,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def load_plan_bundle_json(text: str) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    payload = json.loads(text)
    if int(payload.get("version", 0)) != 1:
        raise ValueError("Unsupported saved plan version")
    return pd.DataFrame(payload["plan"]), pd.DataFrame(payload["investments"]), dict(payload.get("settings", {}))
