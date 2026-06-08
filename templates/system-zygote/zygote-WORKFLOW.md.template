# AI Workflow System Zygote Workflow

<!-- 中文注释：本 Workflow 让当前系统具备生成下一代独立 AI Workflow 工程的能力。 -->

## 目标

从用户提供的系统名称、英文 id、目标、使用者和领域出发，生成一套完全独立的 AI Workflow 工程。

新工程必须默认包含：

- `ai-workflow-system-zygote`
- `ai-workflow-asset-evolution`

## 适用场景

- 用户希望从零创建新的 AI Workflow 工程。
- 用户希望生成一个可以继续自我繁殖和自我演化的系统胚胎。

## 不适用场景

- 只是在已有系统中新增或更新某个资产，此时应使用 `ai-workflow-asset-evolution`。

## 输入

- 系统名称
- 系统英文 id
- 系统目标
- 目标使用者
- 服务领域
- 输出目录

## 输出

- 独立 AI Workflow 工程目录
- 初始化结果 JSON

## 执行步骤

1. 确认用户目标是创建全新 AI Workflow 工程。
2. 收集系统名称、英文 id、目标、使用者和领域。
3. 运行 `workflows/ai-workflow-system-zygote/executors/init_system.py`。
4. 验证生成目录、入口、Router、自复制 Workflow 和资产演化 Workflow。
5. 向用户报告新工程入口。

## 成功标准

- 新工程可独立存在。
- 新工程包含 zygote 和资产演化两个 Workflow。
- 新工程不包含母体品牌文案。
