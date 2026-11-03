#!/usr/bin/env python3
"""Validate that an intent markdown file has required Spec-Driven sections."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_KEYWORDS = [
    ("Background / Why", ["background", "motivation", "why"]),
    ("Core Objectives / What", ["objective", "what", "goal"]),
    ("Guardrails / Anti-Goals", ["guardrail", "anti-goal", "out of scope", "what not"]),
    ("Success Criteria", ["success criteria", "outcomes", "acceptance"]),
]


def validate_intent(path: Path) -> list[str]:
    if not path.exists():
        return [f"File does not exist: {path}"]

    text = path.read_text(encoding="utf-8")
    headings = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip().startswith("#")
    ]

    missing: list[str] = []
    if not headings:
        missing.append("Document has no Markdown headings ('# ...').")
        return missing

    for section_label, keywords in REQUIRED_KEYWORDS:
        if not any(any(kw in h for kw in keywords) for h in headings):
            missing.append(f"Missing required section heading for: {section_label}")

    return missing


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 validate_intent.py <path-to-intent.md>", file=sys.stderr)
        return 2

    target = Path(argv[1])
    issues = validate_intent(target)
    if issues:
        print(f"[FAIL] Intent validation failed for {target}:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print(f"[OK] Intent file '{target}' passed all structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
