# AI Workflow System Zygote Evolution Router

```yaml
id: ai-workflow-system-zygote-evolution
status: active
priority: 98
description: 修改、升级和验证 AI Workflow system zygote 生成机制。

match:
  explicit_mentions:
    any:
      - workflows/ai-workflow-system-zygote-evolution/WORKFLOW.md
      - workflows/ai-workflow-system-zygote/executors/init_system.py
      - rules/workflow/system-zygote-evolution.md
  user_intent:
    any:
      - 修改 zygote
      - 升级 zygote
      - zygote evolution
      - 修改系统胚胎生成过程

route_result:
  route_id: ai-workflow-system-zygote-evolution
  confidence: high
  reason:
    - 用户请求影响 zygote 生成机制
  workflow: workflows/ai-workflow-system-zygote-evolution/WORKFLOW.md
  primary_skill: skills/system-zygote-evolution/SKILL.md
  agents:
    - agents/factory/zygote-evolution-agent/AGENT.md
  rules:
    - rules/workflow/system-zygote-evolution.md
    - rules/workflow/ai-workflow-definition.md
  schemas:
    - schemas/workflow/system-zygote-evolution-result.schema.json
  templates: []
  knowledge:
    - docs/ai-workflow-definition.md
  executor:
    path: null
    required: false
  avoid:
    - workflows/ai-workflow-asset-evolution/WORKFLOW.md
  fallback: ai-context/MISS.md
```
