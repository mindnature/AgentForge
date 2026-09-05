# Changelog

## v0.2.0 — Autonomous Discovery & Architecture Loop

- 新增九阶段有状态项目循环：DISCOVERY → ASSESSMENT → OUTCOME → REDESIGN → ARCHITECTURE → VALIDATION → MVP → SPEC → BUILD。
- 新增 session state、事实来源/置信度、阶段 Gate、自动 next_action 和项目历史。
- 明确普通用户不需要填写 JSON、手动评分或手动推进阶段。
- Red Team 从提示问题升级为可阻断 Agent 架构的降级 Gate。
- 新增结构化 Validator、重试边界和证据要求。
- 新增“最危险假设”MVP 实验结构。
- 扩充 One-page Spec，强制包含需求评级、三条边界、旧/新流程、架构、人机边界、验证、MVP、评测与 Red Team。
- CLI 新增 `start`、`status`、`record-facts`、`set-artifact`、`advance`、`red-team`、`validation-plan`、`mvp`。
- 测试从单一评分/字段检查扩展到状态推进、Red Team 否决、Validation 和 MVP Gate。

## v0.1.0 — Advisor Mode

- 建立痛点深挖、AI Fit、A/B/C/D、流程重设计、组件选型、Validation First、MVP、Red Team 和 One-page Spec 的基础方法论与 CLI。
