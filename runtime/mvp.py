from __future__ import annotations

from typing import Any, Dict

REQUIRED = ["dangerous_assumption", "hypothesis", "sample", "baseline", "success_criteria", "failure_action", "pass_action"]


def build_mvp_experiment(payload: Dict[str, Any]) -> Dict[str, Any]:
    missing = [key for key in REQUIRED if payload.get(key) in (None, "", [], {})]
    if missing:
        raise ValueError(f"missing MVP fields: {', '.join(missing)}")
    return {
        "dangerous_assumption": payload["dangerous_assumption"],
        "hypothesis": payload["hypothesis"],
        "sample": payload["sample"],
        "baseline": payload["baseline"],
        "procedure": payload.get("procedure", []),
        "success_criteria": payload["success_criteria"],
        "failure_action": payload["failure_action"],
        "pass_action": payload["pass_action"],
        "time_budget": payload.get("time_budget"),
        "cost_budget": payload.get("cost_budget")
    }
