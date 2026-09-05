from __future__ import annotations

from typing import Any, Dict, Iterable, List

LEVELS = {"L1", "L2", "L3", "L4", "L5"}
FAILURE_ACTIONS = {"repair", "retry", "block", "human_gate", "warn"}


def build_validation_plan(checks: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    plan: List[Dict[str, Any]] = []
    for index, raw in enumerate(checks, start=1):
        level = str(raw.get("level", "")).upper()
        if level not in LEVELS:
            raise ValueError(f"check {index} has invalid level: {level}")
        name = str(raw.get("name", "")).strip()
        method = str(raw.get("method", "")).strip()
        pass_condition = str(raw.get("pass_condition", "")).strip()
        failure_action = str(raw.get("failure_action", "block")).strip()
        if not name or not method or not pass_condition:
            raise ValueError(f"check {index} requires name, method and pass_condition")
        if failure_action not in FAILURE_ACTIONS:
            raise ValueError(f"check {index} has invalid failure_action: {failure_action}")
        plan.append({
            "id": raw.get("id", f"V{index:02d}"),
            "level": level,
            "name": name,
            "object": raw.get("object"),
            "method": method,
            "pass_condition": pass_condition,
            "failure_action": failure_action,
            "max_retries": int(raw.get("max_retries", 0)),
            "evidence_required": bool(raw.get("evidence_required", level in {"L3", "L4"}))
        })
    if not plan:
        raise ValueError("validation plan must contain at least one check")
    return plan


def validate_retry_policy(plan: List[Dict[str, Any]], global_retry_budget: int = 3) -> Dict[str, Any]:
    if global_retry_budget < 0:
        raise ValueError("global_retry_budget must be >= 0")
    total_declared = sum(max(0, int(item.get("max_retries", 0))) for item in plan)
    return {
        "global_retry_budget": global_retry_budget,
        "declared_path_retries": total_declared,
        "bounded": total_declared <= global_retry_budget or global_retry_budget == 0,
        "stop_rule": "same_failure_without_new_evidence_must_stop_or_change_path"
    }
