# Reprogramming Upstream Sync Record

## 变更目标

明确本仓库作为临时孵化器接入目标项目的使用方式，并将母体升级同步职责纳入 `ai-workflow-system-reprogramming`。

## 变更内容

- `README.md` 增加临时接入方式：clone 或复制到目标项目，完成新建或升级后可删除临时母体副本。
- `templates/system-zygote/README.md.template` 同步接入方式，保证新系统继承该说明。
- `workflows/ai-workflow-system-reprogramming/WORKFLOW.md` 增加母体升级同步、分叉演化识别、资产对比和人工裁决步骤。
- `templates/system-zygote/reprogramming-WORKFLOW.md.template` 同步新版重编程流程。
- `skills/system-reprogramming/SKILL.md` 和模板 Skill 增加识别本地演化资产与避免静默覆盖职责。
- `rules/workflow/system-reprogramming.md` 和模板 Rule 增加母体升级同步约束。

## 设计结论

下游项目同步本仓库升级时，不需要把本仓库作为永久依赖。应临时接入本仓库，执行 `ai-workflow-system-reprogramming`，由目标项目生成或升级自己的 zygote、四个元能力、Harness 和 Eval。执行完成后，临时母体副本可由用户自行删除。

## 验证结果

- 已用 zygote 生成临时样例系统 `reprogramming-sync-test-20260609`。
- 样例系统 README 已继承临时接入方式。
- 样例系统 `ai-workflow-system-reprogramming` 已继承母体升级同步语义。
- 样例系统包含四个元能力、Harness 和 Eval。
- 临时样例系统已清理，不作为项目资产保留。
