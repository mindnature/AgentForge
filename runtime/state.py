from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, MutableMapping
import json
import uuid

STAGES = [
    "DISCOVERY",
    "ASSESSMENT",
    "OUTCOME",
    "REDESIGN",
    "ARCHITECTURE",
    "VALIDATION",
    "MVP",
    "SPEC",
    "BUILD",
]

DISCOVERY_PRIORITY = [
    "target_user",
    "pain_point",
    "trigger_frequency",
    "current_cost",
    "current_workflow",
    "desired_outcome",
    "inputs",
    "human_responsibility",
]

QUESTION_BANK = {
    "target_user": "谁会实际使用这个系统？如果主要是你自己，也请直接说。",
    "pain_point": "现在最麻烦、最耗时或最容易出错的具体环节是什么？",
    "trigger_frequency": "这个任务大概多久发生一次？一次通常处理多少量？",
    "current_cost": "现在完成一次大概要花多少时间、费用或人工检查成本？",
    "current_workflow": "你现在通常怎么完成这件事？把主要步骤简单说一下即可。",
    "desired_outcome": "最后你最希望直接拿到什么可使用的结果？",
    "inputs": "系统实际能拿到哪些输入、文件、数据源或账号权限？",
    "human_responsibility": "哪些判断、发布、付款、删除或最终责任必须由人保留？",
}

STAGE_REQUIRED_ARTIFACTS = {
    "ASSESSMENT": ["assessment"],
    "OUTCOME": ["outcome_definition"],
    "REDESIGN": ["redesigned_workflow"],
    "ARCHITECTURE": ["architecture", "red_team"],
    "VALIDATION": ["validation_plan", "human_boundary"],
    "MVP": ["mvp_experiment"],
    "SPEC": ["one_page_spec"],
    "BUILD": ["build_approved"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_session(idea: str) -> Dict[str, Any]:
    idea = str(idea).strip()
    if not idea:
        raise ValueError("idea must not be empty")
    now = utc_now()
    return {
        "schema_version": "0.2",
        "session_id": str(uuid.uuid4()),
        "idea": idea,
        "stage": "DISCOVERY",
        "status": "active",
        "facts": {},
        "artifacts": {},
        "history": [{"at": now, "event": "session_started", "idea": idea}],
        "created_at": now,
        "updated_at": now,
    }


def _normalize_fact(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping) and "value" in value:
        confidence = float(value.get("confidence", 1.0))
        return {
            "value": value.get("value"),
            "source": value.get("source", "user"),
            "confidence": max(0.0, min(confidence, 1.0)),
            "confirmed": bool(value.get("confirmed", value.get("source", "user") == "user")),
        }
    return {"value": value, "source": "user", "confidence": 1.0, "confirmed": True}


def record_facts(state: MutableMapping[str, Any], facts: Mapping[str, Any]) -> MutableMapping[str, Any]:
    if not isinstance(facts, Mapping):
        raise ValueError("facts must be an object")
    bucket = state.setdefault("facts", {})
    changed: List[str] = []
    for key, raw in facts.items():
        normalized = _normalize_fact(raw)
        if normalized["value"] in (None, "", [], {}):
            continue
        bucket[key] = normalized
        changed.append(key)
    if changed:
        state.setdefault("history", []).append({"at": utc_now(), "event": "facts_recorded", "keys": changed})
        state["updated_at"] = utc_now()
    return state


def fact_value(state: Mapping[str, Any], key: str, default: Any = None) -> Any:
    item = state.get("facts", {}).get(key)
    if isinstance(item, Mapping) and "value" in item:
        return item.get("value", default)
    return default


def discovery_gaps(state: Mapping[str, Any], confidence_floor: float = 0.65) -> List[str]:
    gaps = []
    facts = state.get("facts", {})
    for key in DISCOVERY_PRIORITY:
        item = facts.get(key)
        if not isinstance(item, Mapping) or item.get("value") in (None, "", [], {}):
            gaps.append(key)
            continue
        if item.get("source") == "inferred" and float(item.get("confidence", 0.0)) < confidence_floor:
            gaps.append(key)
    return gaps


def next_questions(state: Mapping[str, Any], max_questions: int = 3) -> List[Dict[str, str]]:
    if state.get("stage") != "DISCOVERY":
        return []
    return [{"field": key, "question": QUESTION_BANK[key]} for key in discovery_gaps(state)[: max(0, int(max_questions))]]


def discovery_ready(state: Mapping[str, Any]) -> bool:
    required = ["target_user", "pain_point", "trigger_frequency", "current_cost", "desired_outcome"]
    return all(fact_value(state, key) not in (None, "", [], {}) for key in required)


def set_artifact(state: MutableMapping[str, Any], name: str, value: Any) -> MutableMapping[str, Any]:
    name = str(name).strip()
    if not name:
        raise ValueError("artifact name must not be empty")
    state.setdefault("artifacts", {})[name] = value
    state.setdefault("history", []).append({"at": utc_now(), "event": "artifact_set", "name": name})
    state["updated_at"] = utc_now()
    return state


def stage_ready(state: Mapping[str, Any], stage: str | None = None) -> bool:
    stage = stage or str(state.get("stage"))
    if stage == "DISCOVERY":
        return discovery_ready(state)
    required = STAGE_REQUIRED_ARTIFACTS.get(stage, [])
    artifacts = state.get("artifacts", {})
    return all(artifacts.get(key) not in (None, "", [], {}) for key in required)


def advance(state: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    stage = str(state.get("stage"))
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage}")
    if not stage_ready(state, stage):
        raise ValueError(f"stage {stage} is not ready")
    if stage == "BUILD":
        state["status"] = "build_ready"
        state["updated_at"] = utc_now()
        return state
    new_stage = STAGES[STAGES.index(stage) + 1]
    state["stage"] = new_stage
    state.setdefault("history", []).append({"at": utc_now(), "event": "stage_advanced", "from": stage, "to": new_stage})
    state["updated_at"] = utc_now()
    return state


def next_action(state: Mapping[str, Any], max_questions: int = 3) -> Dict[str, Any]:
    stage = str(state.get("stage"))
    if stage == "DISCOVERY":
        questions = next_questions(state, max_questions=max_questions)
        if not discovery_ready(state):
            return {"type": "ask", "stage": stage, "questions": questions, "reason": "missing_decision_relevant_discovery_facts"}
        return {"type": "advance", "stage": stage, "to": "ASSESSMENT"}
    if not stage_ready(state, stage):
        action_map = {
            "ASSESSMENT": "run_assessment",
            "OUTCOME": "define_outcome",
            "REDESIGN": "redesign_workflow",
            "ARCHITECTURE": "choose_architecture_and_run_red_team",
            "VALIDATION": "design_validation_and_human_boundary",
            "MVP": "design_mvp",
            "SPEC": "build_one_page_spec",
            "BUILD": "request_explicit_build_approval",
        }
        return {"type": "work", "stage": stage, "action": action_map.get(stage, "complete_stage_artifacts")}
    if stage == "BUILD":
        return {"type": "build", "stage": stage}
    return {"type": "advance", "stage": stage, "to": STAGES[STAGES.index(stage) + 1]}


def session_snapshot(state: Mapping[str, Any], max_questions: int = 3) -> Dict[str, Any]:
    return {
        "session_id": state.get("session_id"),
        "stage": state.get("stage"),
        "status": state.get("status"),
        "facts": deepcopy(state.get("facts", {})),
        "artifact_keys": sorted(state.get("artifacts", {}).keys()),
        "next_action": next_action(state, max_questions=max_questions),
    }


def save_session(state: Mapping[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_session(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
