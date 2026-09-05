from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .scoring import evaluate, load_policy


def redesign_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize a user-provided current workflow into AI-native redesign actions.

    The function intentionally does not invent steps. It validates and normalizes
    action labels so the LLM/Agent can reason over a stable structure.
    """
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
            "replacement": step.get("replacement")
        })
    return result


def architecture_check(components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return warnings when a more deterministic component may be sufficient."""
    warnings = []
    for component in components:
        kind = component.get("kind")
        name = component.get("name", "unnamed")
        deterministic = bool(component.get("deterministic"))
        fixed_path = bool(component.get("fixed_path"))
        if kind == "agent" and deterministic:
            warnings.append({"component": name, "warning": "deterministic_task_should_prefer_program_or_tool"})
        elif kind == "agent" and fixed_path:
            warnings.append({"component": name, "warning": "fixed_path_should_prefer_workflow"})
    return warnings


def build_one_page_spec(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "project_name", "target_user", "pain_point", "trigger_frequency",
        "current_cost", "input", "final_outcome", "acceptance_criteria",
        "risk_nodes", "mvp_experiment"
    ]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError(f"missing spec fields: {', '.join(missing)}")

    spec = {key: payload.get(key) for key in required}
    spec["architecture"] = payload.get("architecture", {})
    spec["validation"] = payload.get("validation", {})
    spec["human_gates"] = payload.get("human_gates", [])
    spec["stop_conditions"] = payload.get("stop_conditions", [])
    spec["evaluation_set"] = payload.get("evaluation_set", {})
    return spec


def project_assessment(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = evaluate(payload["scores"])
    return {
        "assessment": score,
        "outcome_definition": payload.get("outcome_definition"),
        "current_workflow": redesign_steps(payload.get("current_workflow", [])),
        "architecture_warnings": architecture_check(payload.get("components", [])),
        "red_team_questions": load_policy()["red_team_questions"],
    }


def write_json(data: Dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
