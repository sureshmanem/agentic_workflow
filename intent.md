# Intent: TaskPulse — Lightweight Developer Sprint & Task Tracker

## 1. Background & Motivation ("The Why")
Developers working inside agentic workflows need a fast, local-first CLI tool to track tasks, bugs, and sprint progress right inside their repository without context-switching to external SaaS boards or installing heavy runtime dependencies.

This `intent.md` serves as the **Product Source of Truth** in our Intent-Driven / Spec-Driven Development workflow. Any AI agent or developer proposing features must align with these objectives and respect the anti-goals below.

## 2. Core Objectives ("The What")
- Provide a zero-dependency CLI (`python3 -m src.cli`) to create, list, complete, and summarize tasks.
- Persist tasks cleanly in a human-readable local JSON file (default: `.taskpulse.json`, overridable via `--db`).
- Keep core domain logic (`src/core/`) completely decoupled from CLI presentation (`src/cli.py`) so future interfaces (MCP server, TUI, or web UI) can reuse the exact same engine.

## 3. Guardrails & Anti-Goals ("What NOT to Build")
- **Zero third-party packages**: Use Python 3.9+ standard library only (`argparse`, `dataclasses`, `json`, `pathlib`, `unittest`). Do NOT add `pip` dependencies unless an approved intent explicitly lifts this constraint.
- **No external database servers**: Do NOT introduce PostgreSQL, Redis, or cloud sync in v1.
- **No silent mutations**: Every CLI mutation (`add`, `done`) must return a deterministic confirmation message and exit code `0` on success or non-zero on validation error.

## 4. Success Criteria
1. Creating, listing, completing, and summarizing tasks works end-to-end via `python3 -m src.cli`.
2. All unit tests pass via `python3 -m unittest discover -s tests -v` in under 1 second.
3. Architectural audit script (`python3 .agents/skills/quality-check/scripts/audit_repo.py`) passes with zero violations.
