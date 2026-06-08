# AI Workflow Zygote

<!-- 中文注释：本文件是新 AI Workflow 工程的人类入口说明。 -->

`AI Workflow Zygote` 是一套面向 AI workflow systems 的 AI Workflow 工程。

## 项目定位

AI Workflow Zygote 是一个 HARNESS-first 的 AI Workflow 孵化器，用于生成、分化和自我升级可路由、可验证、可反哺的 AI Workflow 系统。

## 系统目标

提供一套通用 AI Workflow 系统胚胎，用于独立生成、演化、重编程和验证 AI Workflow 工程。

## 目标使用者

AI workflow builders

## 接入方式

本仓库推荐作为临时孵化器接入目标项目，而不是作为长期运行依赖。

典型方式：

1. 在需要新建或升级 AI Workflow 系统时，clone 本仓库。
2. 将本仓库文件复制到目标项目的工作目录中，或在目标项目旁作为临时工作副本使用。
3. 通过 `ai-context/ENTRY.md` 启动 Router，并按命中的 Workflow 执行新建、重编程或升级。
4. 执行完成后，目标项目应已经拥有自己的 zygote、元能力、Harness、Eval 和本地资产。
5. 用户可自行删除临时复制进来的母体文件或临时 clone 目录。

已有项目同步本仓库升级时，应使用 `ai-workflow-system-reprogramming`：它负责识别目标项目中既有的 zygote、Workflow、Skill、Agent、Rule、Schema、Template、Harness 和 Eval，并在保留本地演化内容的前提下补齐或迁移新版元能力。

## 运行模型

```text
User Prompt
  -> ai-context / Entry
  -> Router
  -> Workflow
  -> Skill
  -> Agent / Executor
  -> Structured Output
  -> Validation / Eval
  -> Trace / Feedback
```

## 顶层目录

```text
ai-context/     AI 启动入口、任务路由和未命中处理
workflows/      端到端工作流
skills/         可复用流程节点
agents/         智能执行节点
rules/          横切约束
schemas/        输入输出契约
templates/      交付物模板
knowledge/      背景知识和参考资产
adapters/       AI 宿主环境接入方式
evals/          验收和评估标准
docs/           给人类阅读的解释文档
build-process/  本系统自身构建记录
```

## 四个元能力

```text
ai-workflow-system-zygote
  从零生成下一代 AI Workflow 系统

ai-workflow-system-zygote-evolution
  修改、升级和验证 zygote 生成机制

ai-workflow-asset-evolution
  在已有系统中演化 Workflow、Skill、Agent、Rule、Schema、Template 等资产

ai-workflow-system-reprogramming
  将旧项目、不完整 AI 项目或旧 zygote 生成物重编程为完整 AI Workflow 系统
```
