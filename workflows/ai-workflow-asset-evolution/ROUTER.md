# AI Workflow Asset Evolution Router

<!-- 中文注释：本文件是资产演化 Workflow 的轻量路由文件。 -->

```yaml
id: ai-workflow-asset-evolution
status: active
priority: 90
description: 在已有系统中新增、更新和沉淀 AI Workflow 资产。

match:
  explicit_mentions:
    any:
      - workflows/ai-workflow-asset-evolution/WORKFLOW.md
      - rules/workflow/asset-evolution.md

  workspace_signals:
    any:
      - exists: workflows/
      - exists: skills/
      - exists: agents/
      - exists: rules/

  user_intent:
    any:
      - 构建 Workflow
      - 更新 Workflow
      - 沉淀 AI Workflow
      - 设计 Skill
      - 设计 Agent
      - 设计 Rule

  negative_signals:
    any:
      - 用户明确要求从零创建完整系统

route_result:
  route_id: ai-workflow-asset-evolution
  confidence: high
  reason:
    - 用户请求涉及本系统资产演化
  workflow: workflows/ai-workflow-asset-evolution/WORKFLOW.md
  primary_skill: skills/workflow-asset-evolution/SKILL.md
  agents: []
  rules:
    - rules/workflow/asset-evolution.md
  schemas: []
  templates: []
  knowledge: []
  executor:
    path: null
    required: false
  avoid:
    - build-process/
  fallback: ai-context/MISS.md
```
