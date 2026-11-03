---
name: quality-check
description: >-
  Use this skill when asked to audit repository quality, verify architectural
  rules in AGENTS.md, run pre-commit health checks, or validate agentic
  configuration files (.agents/, SKILL.md, intent.md).
---

# Repository Quality & Architecture Check Skill

Run this procedure to verify code health, test pass rates, and `AGENTS.md` compliance across the workspace.

## Execution Steps

1. **Run the Automated Audit Script**:
   Execute [audit_repo.py](./scripts/audit_repo.py):
   ```bash
   python3 .agents/skills/quality-check/scripts/audit_repo.py
   ```
   This script verifies:
   - Required agentic files (`AGENTS.md`, `intent.md`, `.agents/skills/*/SKILL.md`) exist and have valid frontmatter.
   - Domain purity in `src/core/` (no `print(`, `input(`, `sys.exit(`, or `import argparse` calls).
   - Python 3.9+ `from __future__ import annotations` presence in `src/`.

2. **Run Full Unit Test Suite**:
   ```bash
   python3 -m unittest discover -s tests -v
   ```

3. **Report Summary**:
   Present a concise pass/fail table covering Agentic Configs, Domain Purity, and Unit Tests.
