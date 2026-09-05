import pytest
from runtime.state import advance, new_session, next_action, record_facts, set_artifact


def test_raw_idea_starts_with_questions_not_json_form():
    state = new_session("我每天下载很多论文，看不完，想做科研信息助手")
    action = next_action(state)
    assert action["type"] == "ask"
    assert 1 <= len(action["questions"]) <= 3
    assert action["questions"][0]["field"] == "target_user"


def test_discovery_auto_ready_after_minimum_high_impact_facts():
    state = new_session("idea")
    record_facts(state, {"target_user": "我自己", "pain_point": "每天论文太多，筛选耗时", "trigger_frequency": "每天约20篇", "current_cost": "每天约90分钟", "desired_outcome": "得到值得精读的5篇及理由"})
    assert next_action(state) == {"type": "advance", "stage": "DISCOVERY", "to": "ASSESSMENT"}
    advance(state)
    assert state["stage"] == "ASSESSMENT"


def test_stage_cannot_advance_without_artifact():
    state = new_session("idea")
    record_facts(state, {"target_user": "x", "pain_point": "x", "trigger_frequency": "x", "current_cost": "x", "desired_outcome": "x"})
    advance(state)
    with pytest.raises(ValueError):
        advance(state)
    set_artifact(state, "assessment", {"grade": "B"})
    advance(state)
    assert state["stage"] == "OUTCOME"
