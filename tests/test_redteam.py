from runtime.redteam import evaluate_red_team


def test_prompt_coverage_can_block_agent():
    result = evaluate_red_team({"prompt_only_coverage": 85, "workflow_coverage": 90, "agent_added_value": 15, "upgrade_fragility": 20, "no_ai_solution_preferred": False})
    assert result["blocked"] is True
    assert result["recommendation"] == "prefer_prompt_or_skill"


def test_agent_allowed_when_delta_is_real():
    result = evaluate_red_team({"prompt_only_coverage": 35, "workflow_coverage": 55, "agent_added_value": 70, "upgrade_fragility": 30})
    assert result["blocked"] is False
    assert result["recommendation"] == "agent_allowed"
