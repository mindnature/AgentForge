from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .scoring import evaluate, load_policy
from .redteam import evaluate_red_team


def redesign_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    allowed = {"delete", "merge", "parallelize", "postpone", "keep", "human_gate"}
    result = []
    for index, step in enumerate(steps, start=1):
        name = str(step.get("name", "")).strip()
        action = str(step.get("action", "keep")).strip()
        if not name:
            raise ValueError(f"step {index} missing name")
        if action not in allowed:
            raise ValueError(f"step {index} has invalid action: {action}")
        result.append({
            "id": step.get("id", f"S{index:02d}"),
            "name": name,
            "action": action,
            "reason": str(step.get("reason", "")).strip(),
            "replacement": step.get("replacement"),
            "depends_on": step.get("depends_on", [])
        })
    return result


def architecture_check(components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    warnings = []
    for component in components:
        kind = component.get("kind")
        name = component.get("name", "unnamed")
        deterministic = bool(component.get("deterministic"))
        fixed_path = bool(component.get("fixed_path"))
        objective_validator = bool(component.get("objective_validator"))
        if kind == "agent" and deterministic:
            warnings.append({"component": name, "warning": "deterministic_task_should_prefer_program_or_tool"})
        elif kind == "agent" and fixed_path:
            warnings.append({"component": name, "warning": "fixed_path_should_prefer_workflow"})
        if kind == "llm_reviewer" and objective_validator:
            warnings.append({"component": name, "warning": "objective_check_should_prefer_test_or_tool"})
    return warnings

SPEC_REQUIRED = [
    "project_name", "target_user", "pain_point", "trigger_frequency", "current_cost", "input",
    "final_outcome", "acceptance_criteria", "demand_grade", "grade_reasoning", "capability_boundary",
    "cost_boundary", "value_boundary", "dangerous_assumption", "current_workflow", "redesigned_workflow",
    "architecture", "human_boundary", "validation", "retry_policy", "stop_conditions", "mvp_experiment",
    "evaluation_set", "red_team", "recommended_next_step"
]


def build_one_page_spec(payload: Dict[str, Any]) -> Dict[str, Any]:
    missing = [key for key in SPEC_REQUIRED if payload.get(key) in (None, "", [], {})]
    if missing:
        raise ValueError(f"missing spec fields: {', '.join(missing)}")
    if payload["demand_grade"] not in {"A", "B", "C", "D"}:
        raise ValueError("demand_grade must be A/B/C/D")
    red_team = payload["red_team"]
    if isinstance(red_team, dict) and red_team.get("blocked"):
        architecture = payload.get("architecture", {})
        if isinstance(architecture, dict) and architecture.get("primary") == "agent":
            raise ValueError("red team blocked Agent architecture; downgrade before building spec")
    return {key: payload[key] for key in SPEC_REQUIRED}


def project_assessment(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = evaluate(payload["scores"])
    red_team_payload = payload.get("red_team")
    return {
        "assessment": score,
        "outcome_definition": payload.get("outcome_definition"),
        "current_workflow": redesign_steps(payload.get("current_workflow", [])),
        "architecture_warnings": architecture_check(payload.get("components", [])),
        "red_team": evaluate_red_team(red_team_payload) if red_team_payload else None,
        "red_team_questions": load_policy()["red_team_questions"]
    }


def write_json(data: Dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
