import pytest
from runtime.core import architecture_check, build_one_page_spec, redesign_steps


def test_architecture_warns_over_agentization():
    warnings = architecture_check([
        {"name": "排序", "kind": "agent", "deterministic": True, "fixed_path": True},
        {"name": "异常决策", "kind": "agent", "deterministic": False, "fixed_path": False},
    ])
    assert warnings == [{"component": "排序", "warning": "deterministic_task_should_prefer_program_or_tool"}]


def test_redesign_rejects_unknown_action():
    with pytest.raises(ValueError):
        redesign_steps([{"name": "旧步骤", "action": "magic"}])


def test_build_spec_requires_core_fields():
    with pytest.raises(ValueError):
        build_one_page_spec({"project_name": "x"})
