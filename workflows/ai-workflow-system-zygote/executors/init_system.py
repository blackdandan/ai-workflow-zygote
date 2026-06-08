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


def validate(system_path: Path, payload: dict) -> list[str]:
    """零依赖校验生成结果。"""
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
    for item in required_files:
        if not (system_path / item).exists():
            errors.append(f"缺少必要文件：{item}")

    for path in system_path.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if FORBIDDEN_TEXT and FORBIDDEN_TEXT in text.lower():
                errors.append(f"发现禁止品牌字符串：{path}")

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
        return result("failed", system_path, created=created, errors=errors)
    return payload


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
