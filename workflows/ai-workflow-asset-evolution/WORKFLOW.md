# AI Workflow Asset Evolution Workflow

<!-- 中文注释：本 Workflow 负责让新系统具备后续自我演化能力。 -->

## 目标

将本系统中的想法、讨论、规则和流程沉淀为可路由、可执行、可验证、可更新的 AI Workflow 资产。

## 边界

本 Workflow 面向已有工程中的资产演化，不负责从零创建完整系统。

## 适用场景

- 新增 Workflow、Skill、Agent、Rule、Schema 或 Template。
- 更新已有 Workflow 资产。
- 将一次讨论沉淀为正式资产。

## 执行步骤

1. 澄清目标和非目标。
2. 判断内容属于 Workflow、Skill、Agent、Rule、Schema、Template、Knowledge、Evaluation 或 Executor 哪一层。
3. 设计 Workflow Router 和 route result。
4. 设计 Workflow、Skill、Agent、Rule、Schema 和 Template。
5. 对确定性逻辑优先设计 Executor。
6. 形成文件更新计划。
7. 执行更新、验证结果并记录到 docs。

## 文件更新机制

```text
计划 -> 确认 -> 执行 -> 验证 -> 记录
```

## 必须遵守

- `rules/workflow/asset-evolution.md`
- `rules/system-construction/system-construction.md`
