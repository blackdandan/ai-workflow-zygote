# Entry

<!-- 中文注释：Entry 是新系统的最小启动入口，只负责启动 Router。 -->

本文件被调用时，表示 `AI Workflow Zygote` 体系已经启动。

## 启动规则

1. 读取 `ai-context/ROUTER.md`。
2. 按 Router 命中的结果加载对应 Workflow、Skill、Rule、Schema 或 Knowledge。
3. 如果 Router 无法命中，读取 `ai-context/MISS.md`。

## 边界

- 不得绕过 Router 直接执行任务。
- 不得默认加载全部正式资产。
