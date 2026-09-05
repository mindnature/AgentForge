from runtime.state import advance, new_session, record_facts, set_artifact, next_action


def test_one_sentence_can_progress_to_build_approval_gate():
    state = new_session("我每天下载很多论文，看不完，想做一个AI科研信息助手")
    assert next_action(state)["type"] == "ask"
    record_facts(state, {"target_user": "高校科研人员", "pain_point": "每天论文过多，筛选与判断精读价值耗时", "trigger_frequency": "每天20-30篇", "current_cost": "每天90分钟", "desired_outcome": "输出5篇值得精读的论文、理由和证据定位", "inputs": "论文元数据、摘要、PDF", "human_responsibility": "最终收藏与研究方向判断由人负责"})
    advance(state)
    set_artifact(state, "assessment", {"grade": "A", "uncertainty": "精读推荐准确性"}); advance(state)
    set_artifact(state, "outcome_definition", "输入论文材料，交付可验收的精读候选及理由"); advance(state)
    set_artifact(state, "redesigned_workflow", [{"step": "结构化读取"}, {"step": "候选判断"}, {"step": "人工收藏"}]); advance(state)
    set_artifact(state, "architecture", {"primary": "workflow", "agent": "局部不确定判断"})
    set_artifact(state, "red_team", {"blocked": False, "recommendation": "agent_allowed"}); advance(state)
    set_artifact(state, "validation_plan", [{"id": "V01", "check": "证据定位"}])
    set_artifact(state, "human_boundary", {"approve": ["最终收藏"]}); advance(state)
    set_artifact(state, "mvp_experiment", {"sample": "30篇历史论文", "success": "精读候选与人工判断一致"}); advance(state)
    set_artifact(state, "one_page_spec", {"project_name": "PaperScout"}); advance(state)
    action = next_action(state)
    assert action["type"] == "work"
    assert action["action"] == "request_explicit_build_approval"
    set_artifact(state, "build_approved", True)
    assert next_action(state)["type"] == "build"
