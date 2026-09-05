# AgentForge v0.2 方法框架

AgentForge 的工作对象不是“Agent 功能清单”，而是一个尚未被定义清楚的现实问题。v0.2 用有状态循环承载方法论，让用户只负责提供真实上下文，系统负责推进决策。

## 1. Discovery 不等于问卷

先从用户自然语言和已有上下文提取事实，区分 `user` 与 `inferred`。只有会改变需求评级、结果定义、架构、成本、权限或风险的未知才提问，每轮最多 3 个。DISCOVERY 达到最小充分信息就推进，而不是追求字段全满。

## 2. 需求体检

需求侧：频率、时间成本、错误代价、摩擦、可重复性。AI Fit：模型能力、输入可达性、结果可验证性、工具化、自主执行安全性。A/B/C/D 只能作为决策框架，不能用均分掩盖不可逆风险等硬伤。

## 3. 结果重定义

从用户最后要使用的结果反推系统，不把传统步骤和组织角色直接映射为 Agent。

## 4. 流程重设计

对旧流程做 delete、merge、parallelize、postpone、keep、human_gate。特别查找重复搬运、重复摘要、旧审批惯性和可以被 Tool/Test 取代的模型步骤。

## 5. 架构降级优先

组件优先级：Program → Tool → Skill → Workflow → Agent → Human Gate。Agent 需要证明“路径不确定 + 自主判断有额外价值”。

Red Team 是 Gate：非 AI 更优、Prompt/Skill 已覆盖大部分价值、Workflow 已覆盖大部分价值时，必须降级。架构简化不是失败。

## 6. Validation First

每个关键检查项写成：对象、层级、方法、通过条件、失败动作、最大重试、证据。客观问题尽量由规则/Test/Tool处理；L5 才保留价值、审美、重大风险和最终责任判断。

## 7. Human Boundary

澄清处理信息缺口，审批处理授权与外部副作用，质量检查处理结果缺陷。三者不能混在一起。

## 8. MVP 是决策实验

先找最危险假设，再定义样本、Baseline、成功标准、失败动作和通过动作。MVP 的目的，是尽快决定“继续、缩小还是停止”，不是先做一个缩水产品。

## 9. Stateful Loop

阶段状态：DISCOVERY → ASSESSMENT → OUTCOME → REDESIGN → ARCHITECTURE → VALIDATION → MVP → SPEC → BUILD。

每一阶段有可检查的产物 Gate。条件满足后自动推进；用户改约束时只回滚受影响部分。BUILD 必须显式授权。

## 10. 评测 AgentForge 本身

核心 Benchmark 应从一句自然语言开始，而不是预填 JSON。至少覆盖：高频强痛点；低频任务劝退；Prompt/Workflow 足够时降级；高风险动作保留 Human Gate；中途修改约束只重做受影响阶段；验证条件不足时不得伪装进入 Build。
