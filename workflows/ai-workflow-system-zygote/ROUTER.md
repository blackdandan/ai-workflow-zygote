# AI Workflow System Zygote Router

<!-- 中文注释：本文件是系统胚胎 Workflow 的轻量路由文件。 -->

```yaml
id: ai-workflow-system-zygote
status: active
priority: 95
description: 从零创建下一代独立 AI Workflow 工程。

match:
  explicit_mentions:
    any:
      - workflows/ai-workflow-system-zygote/WORKFLOW.md
      - rules/workflow/system-zygote.md

  workspace_signals:
    any:
      - exists: ai-context/
      - exists: workflows/

  user_intent:
    any:
      - 从零创建 AI Workflow 工程
      - 创建下一代系统
      - 创建 zygote
      - 系统胚胎

  negative_signals:
    any:
      - 用户明确要求只更新已有资产

route_result:
  route_id: ai-workflow-system-zygote
  confidence: high
  reason:
    - 用户请求涉及创建下一代独立 AI Workflow 工程
  workflow: workflows/ai-workflow-system-zygote/WORKFLOW.md
  primary_skill: skills/system-zygote/SKILL.md
  agents:
    - agents/factory/system-zygote-agent/AGENT.md
  rules:
    - rules/workflow/system-zygote.md
  schemas: []
  templates:
    - templates/system-zygote/README.md.template
  knowledge: []
  executor:
    path: workflows/ai-workflow-system-zygote/executors/init_system.py
    required: true
  avoid:
    - build-process/
  fallback: ai-context/MISS.md
```
