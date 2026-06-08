# AI Workflow System Reprogramming Workflow

<!-- 中文注释：本 Workflow 用于将旧系统、不完整 AI 项目或已分叉演化的 AI Workflow 系统重编程为完整新版系统。 -->

## 目标

将旧 zygote 生成物、已有但不完整的 AI Workflow 项目、只有基础 AI 规则的项目，或已经从母体分叉并本地演化过的 AI Workflow 项目，重编程为具备新版元能力的完整系统。

本 Workflow 同时承担母体升级同步职责：当本仓库升级后，下游项目可以临时接入本仓库，通过本 Workflow 识别已有 zygote 和本地演化资产，在不覆盖业务内容的前提下补齐、迁移或升级元能力。

## 适用场景

- 旧 zygote 系统缺少新版能力。
- 项目有零散 AI 资产但没有完整 Workflow。
- 项目需要升级为可路由、可验证、可演化的 AI Workflow 系统。
- 下游项目曾使用本仓库孵化，之后自行演化；本仓库也发生升级，需要同步新版元能力。
- 目标项目已经有 zygote、Workflow、Skill、Agent、Rule、Schema、Template、Harness 或 Eval，但版本、结构或语义不一致。

## 接入模型

`ai-workflow-system-reprogramming` 可以通过临时复制或临时 clone 的方式进入目标项目。

执行完成后，目标项目应保留升级后的本地 zygote、四个元能力、Harness、Eval 和迁移记录；临时接入的母体副本可由用户自行删除。

## 执行步骤

1. 诊断目标项目结构。
2. 判断系统类型：空项目、不完整 AI 项目、旧 zygote 项目、已分叉演化项目或新版母体同步项目。
3. 识别目标项目中已有的 zygote、四个元能力、Workflow、Skill、Agent、Rule、Schema、Template、Harness、Eval 和业务资产。
4. 对比当前母体资产与目标项目资产，区分新增、缺失、未改动、本地改动、母体改动和双方都改动的资产。
5. 生成迁移计划，明确每个资产是保留、补齐、升级、合并、转换、标记过时，还是需要人工裁决。
6. 用户确认后补齐和迁移，不得静默覆盖本地演化内容。
7. 验证 Entry、Router、Miss、四个元能力、Harness、Eval、模板继承和本地业务内容。
8. 记录重编程结果，说明临时接入文件是否仍需保留；默认由用户在确认无误后自行删除临时母体副本。

## 成功标准

- 保留原项目业务内容。
- 补齐四个元能力。
- 旧资产有迁移映射。
- Router 可聚合元 Workflow。
- 已有 zygote 和本地演化资产被识别并保留、升级或迁移。
- 母体升级不会静默覆盖目标项目的本地修改。
- 目标项目完成后可独立运行，不依赖临时接入的母体副本。
