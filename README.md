# AgentForge

**Turn a vague pain point into a build-ready AI-native system spec.**

AgentForge 是一个 AI 原生需求架构师。你只需要给它一句需求、痛点或自动化想法，它会先判断这个问题是否值得用 AI 做，再逐步完成痛点深挖、AI Fit、结果重定义、流程重设计、组件选型、验证设计、MVP 和 One-page Spec。

它不以“做出一个 Agent”为成功标准。很多时候，最好的结论可能是：一个 Prompt 就够了，或者固定 Workflow 比 Agent 更可靠。

## 适合解决什么

- “我每天要重复整理很多材料，能不能自动化？”
- “我想做一个科研选题智能体，从哪里开始？”
- “这个业务适不适合做 Agent？”
- “我已经有一个多 Agent 系统，但感觉太复杂，怎么重构？”
- “模型升级以后，哪些旧流程和 Prompt 可以删掉？”

## 核心流程

```text
Pain / Idea
   ↓
Pain Discovery
   ↓
Demand × AI Fit
   ↓
A / B / C / D
   ↓
Outcome Definition
   ↓
Delete / Merge / Parallelize / Postpone
   ↓
Program / Tool / Skill / Workflow / Agent / Human Gate
   ↓
Validation First
   ↓
MVP + Red Team Gate
   ↓
One-page Spec
   ↓
Build (only after approval)
```

## 最重要的设计原则

1. 先定义最终可验收结果，再讨论实现步骤。
2. 能用程序解决，不让模型猜；固定路径优先 Workflow。
3. Agent 只负责那些路径不确定、确实需要自主判断的局部。
4. 先设计“怎么知道它错了”，再提高自主权。
5. 澄清、审批、质量检查是三类不同事件。
6. MVP 验证最危险假设，不先堆完整产品。
7. 系统必须允许结论是“不要做 Agent”。

## 快速开始

将仓库作为 Skill 使用时，可以直接输入：

```text
$agentforge 我每周要整理大量科研项目申报通知，很耗时间，想做成智能体。
```

AgentForge 会先利用你已经提供的信息，只追问少量会改变方案的问题，然后逐阶段推进。

### CLI

```bash
python scripts/agentforge.py score --input examples/research-notice.assessment.json
python scripts/agentforge.py assess --input examples/research-notice.assessment.json
python scripts/agentforge.py build-spec --input examples/research-notice.spec.json
```

运行测试：

```bash
python -m pytest -q
```

## v0.1 范围

当前版本重点是 **Advisor Mode**：把一句想法加工成高质量 One-page Spec，并系统性阻止过度 Agent 化。

下一阶段计划：
- 项目状态与可续跑诊断会话；
- 从 One-page Spec 自动生成 Builder Plan；
- 更严格的成本/风险/验证矩阵；
- 真实评测集与版本对照；
- 与 Codex / Claude Code 等构建环境的受控交接。

## Repository structure

```text
AgentForge/
├── SKILL.md
├── README.md
├── config/
│   └── policy.json
├── runtime/
│   ├── core.py
│   └── scoring.py
├── scripts/
│   └── agentforge.py
├── references/
│   └── method.md
├── schemas/
│   └── assessment.schema.json
├── examples/
│   ├── research-notice.assessment.json
│   └── research-notice.spec.json
└── tests/
```

AgentForge 的目标，是把“我有一个 AI 想法”变成“我知道这个问题值不值得做、该怎么做、怎么验证，以及什么时候不该做”。
