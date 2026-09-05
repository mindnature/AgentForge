from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "policy.json"


def load_policy() -> Dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _validate_dimension(name: str, value: Any, min_value: int, max_value: int) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if value < min_value or value > max_value:
        raise ValueError(f"{name} must be between {min_value} and {max_value}")
    return value


def weighted_score(values: Dict[str, Any], weights: Dict[str, float], scale_min: int = 0, scale_max: int = 5) -> float:
    missing = [key for key in weights if key not in values]
    if missing:
        raise ValueError(f"missing scoring dimensions: {', '.join(missing)}")

    total = 0.0
    for key, weight in weights.items():
        value = _validate_dimension(key, values[key], scale_min, scale_max)
        normalized = (value - scale_min) / (scale_max - scale_min)
        total += normalized * weight
    return round(total * 100, 1)


def classify_grade(need: float, ai_fit: float, verification: float, hard_stop: bool = False) -> str:
    if hard_stop:
        return "D"
    policy = load_policy()
    thresholds = policy["thresholds"]
    if need >= thresholds["A"]["need"] and ai_fit >= thresholds["A"]["ai_fit"] and verification >= thresholds["A"]["verification"]:
        return "A"
    if need >= thresholds["B"]["need"] and ai_fit >= thresholds["B"]["ai_fit"] and verification >= thresholds["B"]["verification"]:
        return "B"
    if need >= thresholds["C"]["need"] and ai_fit >= thresholds["C"]["ai_fit"] and verification >= thresholds["C"]["verification"]:
        return "C"
    return "D"


def evaluate(payload: Dict[str, Any]) -> Dict[str, Any]:
    policy = load_policy()
    scale = policy["scales"]
    need = weighted_score(payload["need"], policy["need_weights"], scale["min"], scale["max"])
    ai_fit = weighted_score(payload["ai_fit"], policy["ai_fit_weights"], scale["min"], scale["max"])
    verification = round(_validate_dimension("verification", payload["verification"], scale["min"], scale["max"]) / scale["max"] * 100, 1)

    hard_reasons = []
    if payload.get("unacceptable_irreversible_risk"):
        hard_reasons.append("unacceptable_irreversible_risk")
    if payload.get("no_real_user_or_trigger"):
        hard_reasons.append("no_real_user_or_trigger")

    grade = classify_grade(need, ai_fit, verification, hard_stop=bool(hard_reasons))
    recommendation = {
        "A": "优先做：进入 AI 原生重设计、MVP 与 One-page Spec。",
        "B": "值得验证：先做小规模真实样本实验，再决定是否完整 Agent 化。",
        "C": "暂不做完整 Agent：优先尝试 Prompt / Skill / Tool / 固定 Workflow。",
        "D": "暂缓：需求、能力、验证性或风险条件尚不成立。"
    }[grade]

    return {
        "grade": grade,
        "need_score": need,
        "ai_fit_score": ai_fit,
        "verification_score": verification,
        "hard_stop_reasons": hard_reasons,
        "recommendation": recommendation,
    }
