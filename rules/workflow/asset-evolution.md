# Workflow Asset Evolution Rule

<!-- 中文注释：本规则约束本系统中的 Workflow 资产演化。 -->

## 适用场景

当需要在 `AI Workflow Zygote` 中新增、更新或沉淀 AI Workflow 资产时，必须遵守本规则。

## 核心原则

### 1. 先分层，再写文件

新增内容前，必须先判断它属于 Workflow、Skill、Agent、Rule、Schema、Template、Knowledge、Evaluation 或 Executor。

### 2. 每个 Workflow 必须可路由

新增 Workflow 必须包含自己的 `ROUTER.md`，并被主 Router 引用。

### 3. 确定性逻辑脚本化

能确定执行的文件操作、结构检查或机械生成，应优先交给 Executor。

### 4. 文件更新必须有计划

文件更新必须遵循：

```text
计划 -> 确认 -> 执行 -> 验证 -> 记录
```

### 5. 完成后必须记录

Workflow 完成后，必须更新 `docs/workflows.md` 或对应记录文档。
