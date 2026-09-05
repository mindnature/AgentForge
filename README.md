# AgentForge

**From one rough pain point to a build-ready AI-native system — with the right to say “don’t build an Agent.”**

AgentForge 是一个有状态的 AI 原生需求架构师。你只需要说一句需求、痛点或自动化想法，它会先利用已有上下文深挖问题，只追问会改变方案的少数关键信息，然后自己推进需求体检、结果定义、流程重设计、架构选型、验证、MVP 和 One-page Spec。

v0.2 的重点，是把 v0.1 的“方法论规则”变成一个可以持续推进的 Autonomous Discovery & Architecture Loop。

## 你可以直接这样开始

```text
$agentforge 我每天下载很多论文，看不完，想做一个 AI 科研信息助手。
```

理想交互不是让你填写几十个字段，而是：

```text
一句痛点
→ AgentForge 提取已知事实
→ 最多追问 1—3 个会改变方案的问题
→ 自动进入需求评级
→ 自动定义可验收结果
→ 自动重设计流程
→ 选择最简单可靠架构
→ Red Team 可以否决 Agent
→ 自动设计 Validator / Human Gate
→ 用 MVP 验证最危险假设
→ 形成 One-page Spec
→ 你明确批准后才进入 Build
```

## v0.2 新增

### Stateful project loop

每个项目持久记录：

`DISCOVERY → ASSESSMENT → OUTCOME → REDESIGN → ARCHITECTURE → VALIDATION → MVP → SPEC → BUILD`

状态里保留已确认事实、推断事实、阶段产物、历史决策和下一动作。用户中途改约束时，只回滚受影响阶段。

### Real Red Team Gate

Red Team 不再只是四个提醒问题。它可以阻断过度 Agent 化：如果 Prompt/Skill 或固定 Workflow 已能覆盖大部分价值，而且 Agent 增量有限，架构必须降级。

### Executable validation structure

Validator 需要明确检查对象、层级、方法、通过条件、失败动作、最大重试和证据要求，避免“再找一个 LLM 看看对不对”。

### Dangerous-assumption MVP

MVP 必须围绕最危险的假设设计真实样本实验，并定义通过/失败后分别做什么。

### Expanded One-page Spec

Spec 现在强制包含需求评级、三条边界、旧/新流程、架构、Human Boundary、Validation、Retry、Stop、MVP、Evaluation Set 和 Red Team 结论。

## 核心原则

1. 先定义最终可验收结果，再讨论实现步骤。
2. 用户负责讲真实问题，AgentForge 负责把自然语言变成结构化判断。
3. 能用程序解决，不让模型猜；固定路径优先 Workflow。
4. 先设计“怎么知道它错了”，再提高自主权。
5. MVP 验证最危险假设，不先堆完整产品。
6. AgentForge 必须允许“不用 Agent / 不用 AI”成为正式结论。
7. Advisor 可以自主推进，Build 必须得到明确批准。

## CLI

CLI 主要服务工程验证和状态持久化，不要求普通用户填写 JSON。

```bash
python scripts/agentforge.py start --idea "我每周整理很多科研通知" --session .agentforge/project.json
python scripts/agentforge.py status --session .agentforge/project.json
python scripts/agentforge.py red-team --input examples/red-team.workflow-enough.json
python scripts/agentforge.py validation-plan --input examples/validation.research-notice.json
python scripts/agentforge.py mvp --input examples/mvp.research-notice.json
```

运行测试：

```bash
python -m pytest -q
```

## Repository structure

```text
AgentForge/
├── SKILL.md
├── README.md
├── config/policy.json
├── runtime/
│   ├── state.py
│   ├── scoring.py
│   ├── redteam.py
│   ├── validation.py
│   ├── mvp.py
│   └── core.py
├── scripts/agentforge.py
├── schemas/
│   ├── assessment.schema.json
│   └── session.schema.json
├── references/method.md
└── tests/
```

AgentForge 的完成标准不是“成功生成了一个 Agent”，而是：从一句模糊痛点开始，最终让用户知道这个问题值不值得做、最小正确架构是什么、怎么验证，以及什么时候不该做。
