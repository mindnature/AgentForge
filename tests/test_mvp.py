import pytest
from runtime.mvp import build_mvp_experiment


def test_mvp_requires_decision_actions():
    with pytest.raises(ValueError):
        build_mvp_experiment({"dangerous_assumption": "AI能稳定提取关键条件"})


def test_mvp_is_experiment_not_feature_list():
    result = build_mvp_experiment({"dangerous_assumption": "AI能稳定提取关键条件", "hypothesis": "20份历史通知中关键字段无致命遗漏", "sample": "20份历史通知", "baseline": "人工整理结果", "success_criteria": "关键字段准确率>=98%，致命遗漏=0", "failure_action": "缩小自动化范围", "pass_action": "进入固定Workflow原型"})
    assert "success_criteria" in result
    assert result["failure_action"] == "缩小自动化范围"
