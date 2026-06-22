#!/usr/bin/env python3
"""
AI Workflow 系统胚胎初始化执行器。

本脚本用于从模板生成一个完全独立的 AI Workflow 工程。
脚本不与用户交互，必须由 Agent 先收集系统名称、英文 id、目标、使用者和领域。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FORBIDDEN_TEXT = ""
VALID_ID = re.compile(r"^[a-z][a-z0-9-]*$")


def result(status: str, system_path: Path, *, created=None, warnings=None, errors=None, next_entry=None) -> dict:
    """生成统一 JSON 输出。"""
    return {
        "status": status,
        "system_path": str(system_path),
        "created_files": created or [],
        "warnings": warnings or [],
        "errors": errors or [],
        "next_entry": next_entry,
    }


def render(template: str, values: dict[str, str]) -> str:
    """替换模板占位符。"""
    output = template
    for key, value in values.items():
        output = output.replace("{{" + key + "}}", value)
    return output


def write(path: Path, content: str, created: list[str]) -> None:
    """写入文件并记录路径。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))


def read_template(base: Path, name: str) -> str:
    """读取 zygote 模板。"""
    return (base / "templates/system-zygote" / name).read_text(encoding="utf-8")


def ensure_dirs(system_path: Path) -> None:
    """创建新系统的基础目录。"""
    dirs = [
        "ai-context",
        "workflows/ai-workflow-system-zygote/executors",
        "workflows/ai-workflow-system-zygote-evolution",
        "workflows/ai-workflow-asset-evolution",
        "workflows/ai-workflow-system-reprogramming",
        "skills/system-zygote/subskills",
        "skills/system-zygote-evolution/subskills",
        "skills/workflow-asset-evolution/subskills",
        "skills/system-reprogramming/subskills",
        "agents/factory/system-zygote-agent",
        "agents/factory/zygote-evolution-agent",
        "agents/factory/workflow-asset-agent",
        "agents/factory/system-reprogramming-agent",
        "rules/system-construction",
        "rules/agent",
        "rules/harness",
        "rules/workflow",
        "schemas/workflow",
        "schemas/outputs",
        "schemas/project",
        "templates/system-zygote",
        "templates/workflow-spec",
        "templates/skill-spec",
        "templates/agent-spec",
        "knowledge",
        "adapters",
        "evals",
        "evals/workflow",
        "evals/agent",
        "evals/output-quality",
        "docs",
        "build-process/records",
    ]
    for item in dirs:
        (system_path / item).mkdir(parents=True, exist_ok=True)

# Helper functions for validation
def parse_yaml_subset(text: str) -> dict | list:
    """零依赖简易 YAML 解析器，用于解析路由和清单文件。
    支持：字典键值对、嵌套缩进块、列表（以 - 开头）、基础标量类型（bool, int, float, null, str）。
    """
    lines = []
    for line_num, raw_line in enumerate(text.splitlines(), 1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        
        # 移除行内注释（检测在引号外的 #）
        comment_idx = -1
        in_quote = None
        for idx, char in enumerate(raw_line):
            if char in ("'", '"'):
                if in_quote == char:
                    in_quote = None
                elif in_quote is None:
                    in_quote = char
            elif char == '#' and in_quote is None:
                comment_idx = idx
                break
        
        if comment_idx != -1:
            raw_line = raw_line[:comment_idx]
            stripped = raw_line.strip()
            if not stripped:
                continue

        leading = raw_line[:len(raw_line) - len(raw_line.lstrip(' \t'))]
        if '\t' in leading:
            raise ValueError(f"第 {line_num} 行: YAML 禁止使用 Tab 缩进")
        indent = len(leading)
        lines.append((line_num, indent, raw_line.strip()))
        
    if not lines:
        return {}

    def parse_block(start_idx: int, end_idx: int):
        first_line_num, first_indent, first_content = lines[start_idx]
        
        if first_content.startswith('-'):
            result_list = []
            i = start_idx
            while i <= end_idx:
                line_num, indent, content = lines[i]
                if indent != first_indent:
                    raise ValueError(f"第 {line_num} 行: 缩进不匹配，预期为 {first_indent}，实际为 {indent}")
                if not content.startswith('-'):
                    raise ValueError(f"第 {line_num} 行: 列表项应以 '-' 开头")
                
                val_str = content[1:].strip()
                item_end = i
                while item_end + 1 <= end_idx and lines[item_end + 1][1] > first_indent:
                    item_end += 1
                
                if item_end > i:
                    val = parse_block(i + 1, item_end)
                    if val_str:
                        raise ValueError(f"第 {line_num} 行: 列表项开头和嵌套缩进冲突")
                else:
                    val = parse_scalar(val_str, line_num)
                
                result_list.append(val)
                i = item_end + 1
            return result_list
        else:
            result_dict = {}
            i = start_idx
            while i <= end_idx:
                line_num, indent, content = lines[i]
                if indent != first_indent:
                    raise ValueError(f"第 {line_num} 行: 缩进不匹配，预期为 {first_indent}，实际为 {indent}")
                
                if ':' not in content:
                    raise ValueError(f"第 {line_num} 行: 字典项缺少冒号 ':'")
                
                key_part, val_part = content.split(':', 1)
                key = key_part.strip()
                if not key:
                    raise ValueError(f"第 {line_num} 行: 键名不能为空")
                if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
                    key = key[1:-1]
                
                val_str = val_part.strip()
                item_end = i
                while item_end + 1 <= end_idx and lines[item_end + 1][1] > first_indent:
                    item_end += 1
                
                if item_end > i:
                    val = parse_block(i + 1, item_end)
                    if val_str:
                        raise ValueError(f"第 {line_num} 行: 键已具有行内值，不能包含嵌套块")
                else:
                    val = parse_scalar(val_str, line_num)
                
                if key in result_dict:
                    raise ValueError(f"第 {line_num} 行: 重复的键 '{key}'")
                result_dict[key] = val
                i = item_end + 1
            return result_dict

    def parse_scalar(val_str: str, line_num: int):
        if not val_str:
            return None
        if val_str == "[]":
            return []
        if val_str == "{}":
            return {}
        if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
            return val_str[1:-1]
        if val_str.lower() in ('true', 'yes', 'on'):
            return True
        if val_str.lower() in ('false', 'no', 'off'):
            return False
        if val_str.lower() == 'null':
            return None
        try:
            if '.' in val_str:
                return float(val_str)
            return int(val_str)
        except ValueError:
            return val_str

    return parse_block(0, len(lines) - 1)


def validate_json_syntax(path: Path) -> list[str]:
    """校验 JSON 文件语法。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        return []
    except Exception as e:
        return [f"JSON 语法错误 ({path.name}): {e}"]


def validate_yaml_syntax(path: Path, is_markdown: bool = False) -> list[str]:
    """校验 YAML / Markdown YAML 块语法。"""
    try:
        content = path.read_text(encoding="utf-8")
        if is_markdown:
            # 提取 ```yaml 与 ``` 之间的内容
            pattern = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
            blocks = pattern.findall(content)
            if not blocks:
                return [f"Markdown 路由文件缺少 ```yaml 块 ({path.name})"]
            errors = []
            for idx, block in enumerate(blocks, 1):
                try:
                    parse_yaml_subset(block)
                except Exception as e:
                    errors.append(f"Markdown 路由第 {idx} 个 YAML 块语法错误 ({path.name}): {e}")
            return errors
        else:
            try:
                parse_yaml_subset(content)
                return []
            except Exception as e:
                return [f"YAML 语法错误 ({path.name}): {e}"]
    except Exception as e:
        return [f"读取/校验 YAML 异常 ({path.name}): {e}"]


def validate(system_path: Path, payload: dict) -> list[str]:
    """零依赖校验生成结果，包含语法与结构验证。"""
    errors: list[str] = []
    required_files = [
        "README.md",
        "ai-context/ENTRY.md",
        "ai-context/ROUTER.md",
        "ai-context/MISS.md",
        "workflows/ai-workflow-system-zygote/ROUTER.md",
        "workflows/ai-workflow-system-zygote/WORKFLOW.md",
        "workflows/ai-workflow-system-zygote/manifest.yaml",
        "workflows/ai-workflow-system-zygote/executors/init_system.py",
        "workflows/ai-workflow-system-zygote-evolution/ROUTER.md",
        "workflows/ai-workflow-system-zygote-evolution/WORKFLOW.md",
        "workflows/ai-workflow-system-zygote-evolution/manifest.yaml",
        "workflows/ai-workflow-asset-evolution/ROUTER.md",
        "workflows/ai-workflow-asset-evolution/WORKFLOW.md",
        "workflows/ai-workflow-asset-evolution/manifest.yaml",
        "workflows/ai-workflow-system-reprogramming/ROUTER.md",
        "workflows/ai-workflow-system-reprogramming/WORKFLOW.md",
        "workflows/ai-workflow-system-reprogramming/manifest.yaml",
        "skills/system-zygote/SKILL.md",
        "skills/system-zygote-evolution/SKILL.md",
        "skills/workflow-asset-evolution/SKILL.md",
        "skills/system-reprogramming/SKILL.md",
        "rules/system-construction/system-construction.md",
        "rules/workflow/system-zygote.md",
        "rules/workflow/system-zygote-evolution.md",
        "rules/workflow/asset-evolution.md",
        "rules/workflow/system-reprogramming.md",
        "rules/workflow/ai-workflow-definition.md",
        "rules/agent/agent-boundary.md",
        "rules/harness/README.md",
        "evals/README.md",
        "docs/workflows.md",
        "docs/ai-workflow-definition.md",
    ]
    
    # 1. 存在性校验
    for item in required_files:
        file_path = system_path / item
        if not file_path.exists():
            errors.append(f"缺少必要文件：{item}")
        else:
            # 2. 深度语法与结构校验
            if item.endswith(".yaml"):
                errors.extend(validate_yaml_syntax(file_path, is_markdown=False))
            elif item.endswith("ROUTER.md"):
                errors.extend(validate_yaml_syntax(file_path, is_markdown=True))
            elif item.endswith(".json") or item.endswith(".schema.json"):
                errors.extend(validate_json_syntax(file_path))

    # 3. 品牌词校验
    for path in system_path.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if FORBIDDEN_TEXT and FORBIDDEN_TEXT in text.lower():
                errors.append(f"发现禁止品牌字符串：{path}")

    # 4. JSON 结构完整性校验
    for field in ["status", "system_path", "created_files", "warnings", "errors", "next_entry"]:
        if field not in payload:
            errors.append(f"结果 JSON 缺少字段：{field}")
    if payload.get("status") not in {"initialized", "failed"}:
        errors.append("结果 JSON status 非法")
        
    return errors


def initialize(args: argparse.Namespace) -> dict:
    """生成新 AI Workflow 工程。"""
    if not VALID_ID.match(args.system_id):
        return result("failed", Path(args.target).resolve() / args.system_id, errors=["system_id 必须使用小写字母、数字和连字符，并以字母开头。"])

    base = Path(__file__).resolve().parents[3]
    target = Path(args.target).resolve()
    system_path = target / args.system_id
    created: list[str] = []

    if system_path.exists():
        return result("failed", system_path, errors=["目标系统目录已存在，脚本不会覆盖已有工程。"])

    import shutil  # 用于异常和校验失败时的回滚清理

    try:
        ensure_dirs(system_path)

        values = {
            "SYSTEM_NAME": args.system_name,
            "SYSTEM_ID": args.system_id,
            "SYSTEM_GOAL": args.system_goal,
            "TARGET_USERS": args.target_users,
            "DOMAIN": args.domain,
        }

        file_map = {
            "README.md.template": "README.md",
            "ENTRY.md.template": "ai-context/ENTRY.md",
            "ROUTER.md.template": "ai-context/ROUTER.md",
            "MISS.md.template": "ai-context/MISS.md",
            "docs-workflows.md.template": "docs/workflows.md",
            "docs-ai-workflow-definition.md.template": "docs/ai-workflow-definition.md",
            "system-construction-rule.md.template": "rules/system-construction/system-construction.md",
            "ai-workflow-definition-rule.md.template": "rules/workflow/ai-workflow-definition.md",
            "agent-boundary-rule.md.template": "rules/agent/agent-boundary.md",
            "harness-README.md.template": "rules/harness/README.md",
            "harness-human-control.md.template": "rules/harness/human-control.md",
            "harness-tool-boundary.md.template": "rules/harness/tool-boundary.md",
            "harness-guardrails.md.template": "rules/harness/guardrails.md",
            "harness-stop-and-ask.md.template": "rules/harness/stop-and-ask.md",
            "evals-README.md.template": "evals/README.md",
            "evals-workflow-README.md.template": "evals/workflow/README.md",
            "evals-agent-README.md.template": "evals/agent/README.md",
            "evals-output-quality-README.md.template": "evals/output-quality/README.md",
            "zygote-WORKFLOW.md.template": "workflows/ai-workflow-system-zygote/WORKFLOW.md",
            "zygote-ROUTER.md.template": "workflows/ai-workflow-system-zygote/ROUTER.md",
            "zygote-manifest.yaml.template": "workflows/ai-workflow-system-zygote/manifest.yaml",
            "zygote-SKILL.md.template": "skills/system-zygote/SKILL.md",
            "zygote-rule.md.template": "rules/workflow/system-zygote.md",
            "zygote-agent.md.template": "agents/factory/system-zygote-agent/AGENT.md",
            "zygote-evolution-WORKFLOW.md.template": "workflows/ai-workflow-system-zygote-evolution/WORKFLOW.md",
            "zygote-evolution-ROUTER.md.template": "workflows/ai-workflow-system-zygote-evolution/ROUTER.md",
            "zygote-evolution-manifest.yaml.template": "workflows/ai-workflow-system-zygote-evolution/manifest.yaml",
            "zygote-evolution-SKILL.md.template": "skills/system-zygote-evolution/SKILL.md",
            "zygote-evolution-rule.md.template": "rules/workflow/system-zygote-evolution.md",
            "zygote-evolution-agent.md.template": "agents/factory/zygote-evolution-agent/AGENT.md",
            "asset-evolution-WORKFLOW.md.template": "workflows/ai-workflow-asset-evolution/WORKFLOW.md",
            "asset-evolution-ROUTER.md.template": "workflows/ai-workflow-asset-evolution/ROUTER.md",
            "asset-evolution-manifest.yaml.template": "workflows/ai-workflow-asset-evolution/manifest.yaml",
            "asset-evolution-SKILL.md.template": "skills/workflow-asset-evolution/SKILL.md",
            "asset-evolution-rule.md.template": "rules/workflow/asset-evolution.md",
            "asset-evolution-agent.md.template": "agents/factory/workflow-asset-agent/AGENT.md",
            "reprogramming-WORKFLOW.md.template": "workflows/ai-workflow-system-reprogramming/WORKFLOW.md",
            "reprogramming-ROUTER.md.template": "workflows/ai-workflow-system-reprogramming/ROUTER.md",
            "reprogramming-manifest.yaml.template": "workflows/ai-workflow-system-reprogramming/manifest.yaml",
            "reprogramming-SKILL.md.template": "skills/system-reprogramming/SKILL.md",
            "reprogramming-rule.md.template": "rules/workflow/system-reprogramming.md",
            "reprogramming-agent.md.template": "agents/factory/system-reprogramming-agent/AGENT.md",
            "system-zygote-evolution-result.schema.json.template": "schemas/workflow/system-zygote-evolution-result.schema.json",
            "system-reprogramming-result.schema.json.template": "schemas/workflow/system-reprogramming-result.schema.json",
        }

        for template_name, output_path in file_map.items():
            content = render(read_template(base, template_name), values)
            write(system_path / output_path, content, created)

        # 将 zygote 模板原样放入新工程，保证新工程可以继续生成下一代。
        template_dir = base / "templates/system-zygote"
        for template_path in template_dir.iterdir():
            if template_path.is_file():
                write(system_path / "templates/system-zygote" / template_path.name, template_path.read_text(encoding="utf-8"), created)

        # 将当前执行器复制为新工程的 zygote 执行器，并移除母体品牌校验值。
        executor_source = Path(__file__).read_text(encoding="utf-8")
        executor_source = executor_source.replace('FORBIDDEN_TEXT = ""', 'FORBIDDEN_TEXT = ""')
        write(system_path / "workflows/ai-workflow-system-zygote/executors/init_system.py", executor_source, created)

        minimal_readmes = {
            "workflows/README.md": "# Workflows\n\n<!-- 中文注释：保存端到端工作流。 -->\n",
            "skills/README.md": "# Skills\n\n<!-- 中文注释：保存可复用流程能力。 -->\n",
            "agents/README.md": "# Agents\n\n<!-- 中文注释：保存智能执行节点。 -->\n",
            "rules/README.md": "# Rules\n\n<!-- 中文注释：保存横切约束。 -->\n",
            "schemas/README.md": "# Schemas\n\n<!-- 中文注释：保存输入输出契约。 -->\n",
            "templates/README.md": "# Templates\n\n<!-- 中文注释：保存可复用模板。 -->\n",
            "knowledge/README.md": "# Knowledge\n\n<!-- 中文注释：保存背景知识。 -->\n",
            "adapters/README.md": "# Adapters\n\n<!-- 中文注释：保存宿主环境适配说明。 -->\n",
            "build-process/README.md": "# Build Process\n\n<!-- 中文注释：保存本系统自身构建记录。 -->\n",
        }
        for output_path, content in minimal_readmes.items():
            write(system_path / output_path, content, created)

        payload = result("initialized", system_path, created=created, next_entry=f"{args.system_id}/ai-context/ENTRY.md")
        errors = validate(system_path, payload)
        if errors:
            # 校验失败执行回滚清理
            if system_path.exists():
                shutil.rmtree(system_path, ignore_errors=True)
            return result("failed", system_path, errors=errors)
        return payload

    except Exception as exc:
        # 生成过程异常执行回滚清理
        if system_path.exists():
            shutil.rmtree(system_path, ignore_errors=True)
        return result("failed", system_path, errors=[f"生成中断已回滚清理。异常信息: {exc}"])


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="生成独立 AI Workflow 工程胚胎。")
    parser.add_argument("--target", default=".", help="新工程生成到哪个目录下。")
    parser.add_argument("--system-name", required=True, help="系统名称。")
    parser.add_argument("--system-id", required=True, help="系统英文 id。")
    parser.add_argument("--system-goal", required=True, help="系统目标。")
    parser.add_argument("--target-users", required=True, help="目标使用者。")
    parser.add_argument("--domain", required=True, help="服务领域。")
    return parser.parse_args()


def main() -> int:
    """脚本入口。"""
    try:
        payload = initialize(parse_args())
    except Exception as exc:  # noqa: BLE001 - 顶层必须输出结构化失败
        payload = result("failed", Path(".").resolve(), errors=[str(exc)])
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")
    return 0 if payload["status"] == "initialized" else 1


if __name__ == "__main__":
    raise SystemExit(main())
