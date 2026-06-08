# AI Workflow System Reprogramming Router

```yaml
id: ai-workflow-system-reprogramming
status: active
priority: 96
description: 将旧项目、不完整 AI 项目或旧 zygote 生成物重编程为完整 AI Workflow 系统。

match:
  explicit_mentions:
    any:
      - workflows/ai-workflow-system-reprogramming/WORKFLOW.md
      - rules/workflow/system-reprogramming.md
  user_intent:
    any:
      - 修复旧 zygote 项目
      - 升级旧 AI Workflow 项目
      - 补齐 AI Workflow 流程
      - 重编程
      - reprogramming

route_result:
  route_id: ai-workflow-system-reprogramming
  confidence: high
  reason:
    - 用户请求涉及旧系统升级或不完整 AI 项目重编程
  workflow: workflows/ai-workflow-system-reprogramming/WORKFLOW.md
  primary_skill: skills/system-reprogramming/SKILL.md
  agents:
    - agents/factory/system-reprogramming-agent/AGENT.md
  rules:
    - rules/workflow/system-reprogramming.md
    - rules/workflow/ai-workflow-definition.md
  schemas:
    - schemas/workflow/system-reprogramming-result.schema.json
  templates: []
  knowledge:
    - docs/ai-workflow-definition.md
  executor:
    path: null
    required: false
  avoid:
    - workflows/ai-workflow-system-zygote/WORKFLOW.md
  fallback: ai-context/MISS.md
```
