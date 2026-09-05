from __future__ import annotations

from typing import Any, Dict, List


def _score(value: Any, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if value < 0 or value > 100:
        raise ValueError(f"{name} must be between 0 and 100")
    return value


def evaluate_red_team(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt_coverage = _score(payload.get("prompt_only_coverage", 0), "prompt_only_coverage")
    workflow_coverage = _score(payload.get("workflow_coverage", 0), "workflow_coverage")
    agent_delta = _score(payload.get("agent_added_value", 0), "agent_added_value")
    upgrade_fragility = _score(payload.get("upgrade_fragility", 0), "upgrade_fragility")
    no_ai_preferred = bool(payload.get("no_ai_solution_preferred", False))

    reasons: List[str] = []
    recommendation = "agent_allowed"
    if no_ai_preferred:
        recommendation = "prefer_non_ai"
        reasons.append("non_ai_solution_is_cheaper_or_more_stable")
    elif prompt_coverage >= 80 and agent_delta <= 20:
        recommendation = "prefer_prompt_or_skill"
        reasons.append("prompt_or_skill_covers_most_value")
    elif workflow_coverage >= 90 and agent_delta <= 25:
        recommendation = "prefer_workflow"
        reasons.append("fixed_workflow_covers_most_value")

    if upgrade_fragility >= 75:
        reasons.append("architecture_is_highly_model_upgrade_fragile")
        if recommendation == "agent_allowed" and agent_delta < 40:
            recommendation = "prefer_workflow"

    return {
        "blocked": recommendation != "agent_allowed",
        "recommendation": recommendation,
        "reasons": reasons,
        "evidence": {
            "prompt_only_coverage": prompt_coverage,
            "workflow_coverage": workflow_coverage,
            "agent_added_value": agent_delta,
            "upgrade_fragility": upgrade_fragility
        }
    }
