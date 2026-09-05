import pytest
from runtime.validation import build_validation_plan


def test_validation_plan_is_executable_structure():
    plan = build_validation_plan([{"level": "L4", "name": "截止时间核验", "object": "deadline", "method": "回到原通知定位原句", "pass_condition": "提取日期与原文一致", "failure_action": "block", "max_retries": 1}])
    assert plan[0]["id"] == "V01"
    assert plan[0]["evidence_required"] is True


def test_validation_rejects_vague_check():
    with pytest.raises(ValueError):
        build_validation_plan([{"level": "L2", "name": "检查一下"}])
