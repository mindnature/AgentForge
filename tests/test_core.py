import pytest
from runtime.core import architecture_check, build_one_page_spec, redesign_steps


def test_architecture_warns_over_agentization():
    warnings = architecture_check([{"name": "排序", "kind": "agent", "deterministic": True, "fixed_path": True}, {"name": "异常决策", "kind": "agent", "deterministic": False, "fixed_path": False}])
    assert warnings[0] == {"component": "排序", "warning": "deterministic_task_should_prefer_program_or_tool"}


def test_red_team_block_prevents_agent_spec():
    payload = {key: "x" for key in ["project_name", "target_user", "pain_point", "trigger_frequency", "current_cost", "input", "final_outcome", "acceptance_criteria", "grade_reasoning", "capability_boundary", "cost_boundary", "value_boundary", "dangerous_assumption", "current_workflow", "redesigned_workflow", "human_boundary", "validation", "retry_policy", "stop_conditions", "mvp_experiment", "evaluation_set", "recommended_next_step"]}
    payload["demand_grade"] = "A"
    payload["architecture"] = {"primary": "agent"}
    payload["red_team"] = {"blocked": True}
    with pytest.raises(ValueError):
        build_one_page_spec(payload)


def test_redesign_rejects_unknown_action():
    with pytest.raises(ValueError):
        redesign_steps([{"name": "旧步骤", "action": "magic"}])
