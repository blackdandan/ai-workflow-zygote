# Router

<!-- 中文注释：主 Router 是路由聚合器，只加载轻量 Workflow Router。 -->

Router 是 `AI Workflow Zygote` 的路由聚合器。

## 路由流程

1. 读取本文件。
2. 读取 `workflow_routers` 中列出的所有 Workflow Router。
3. 根据显式提及、工作区信号、用户意图和项目上下文进行匹配。
4. 命中后，只加载该 Workflow Router 的 `route_result` 中声明的文件。
5. 如果无法命中，读取 `ai-context/MISS.md`。

## Workflow Routers

```yaml
workflow_routers:
  - workflows/ai-workflow-system-zygote/ROUTER.md
  - workflows/ai-workflow-system-zygote-evolution/ROUTER.md
  - workflows/ai-workflow-asset-evolution/ROUTER.md
  - workflows/ai-workflow-system-reprogramming/ROUTER.md
```

## Route Result

```yaml
route_result:
  route_id: string
  confidence: high | medium | low
  reason: []
  workflow: string
  primary_skill: string | null
  agents: []
  rules: []
  schemas: []
  templates: []
  knowledge: []
  executor:
    path: string | null
    required: boolean
  avoid: []
  fallback: ai-context/MISS.md
```
