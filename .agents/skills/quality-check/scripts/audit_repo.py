#!/usr/bin/env python3
"""Audit repository architecture rules (AGENTS.md) and agentic file structure."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def check_domain_purity(core_dir: Path) -> list[str]:
    violations: list[str] = []
    for py_file in sorted(core_dir.glob("*.py")):
        source = py_file.read_text(encoding="utf-8")
        rel = py_file.relative_to(ROOT)

        if py_file.name != "__init__.py" and "from __future__ import annotations" not in source:
            violations.append(f"{rel}: missing 'from __future__ import annotations'")

        tree = ast.parse(source, filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"print", "input"}:
                    violations.append(
                        f"{rel}:{node.lineno}: forbidden '{node.func.id}()' call in pure core layer"
                    )
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "argparse":
                        violations.append(f"{rel}:{node.lineno}: forbidden 'argparse' import in core")
            if isinstance(node, ast.ImportFrom) and node.module == "argparse":
                violations.append(f"{rel}:{node.lineno}: forbidden 'argparse' import in core")
    return violations


def check_agentic_files() -> list[str]:
    violations: list[str] = []
    for required in ["AGENTS.md", "intent.md", "src/core/AGENTS.md"]:
        if not (ROOT / required).exists():
            violations.append(f"Missing required file: {required}")

    skill_files = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
    if not skill_files:
        violations.append("No SKILL.md files found under .agents/skills/*/")
    for skill_md in skill_files:
        text = skill_md.read_text(encoding="utf-8")
        rel = skill_md.relative_to(ROOT)
        if not text.startswith("---\n"):
            violations.append(f"{rel}: SKILL.md must start with YAML frontmatter ('---')")
        if "name:" not in text or "description:" not in text:
            violations.append(f"{rel}: SKILL.md frontmatter must declare 'name' and 'description'")
    return violations


def main() -> int:
    errors = check_agentic_files() + check_domain_purity(ROOT / "src" / "core")
    if errors:
        print("[FAIL] Repository audit found violations:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("[OK] All AGENTS.md rules, SKILL.md frontmatter checks, and src/core/ purity checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
