# System Zygote Skill

<!-- 中文注释：本 Skill 负责把用户意图转化为一个新的独立 AI Workflow 工程。 -->

## 使用场景

当用户希望从零创建下一代 AI Workflow 工程时，使用本 Skill。

## 职责

- 收集系统名称、英文 id、目标、使用者和领域。
- 调用 `init_system.py` 生成新系统。
- 检查新系统是否包含 zygote 和资产演化能力。

## 输出

- 独立 AI Workflow 工程目录
- 初始化结果 JSON
