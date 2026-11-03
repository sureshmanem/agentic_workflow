# Repository Agent Rules (`AGENTS.md`)

Welcome, Agent. This file is the **always-on operating manual** for this repository. Follow these rules in every session.

## Project Overview
**TaskPulse** is a zero-dependency Python CLI task tracker designed as a reference architecture for **Agentic Workflows** (`intent.md`, `AGENTS.md`, `SKILL.md`, custom subagents, and lifecycle hooks).

## Environment & Commands
- **Language**: Python 3.9+ (standard library **only** — no `pip` packages).
- **Compatibility**: Always include `from __future__ import annotations` at the top of every Python module so modern union/generic type annotations (`str | None`, `list[Task]`) work on Python 3.9+.
- **Run CLI**: `python3 -m src.cli --help`
- **Run Unit Tests**: `python3 -m unittest discover -s tests -v`
- **Run Repo Audit**: `python3 .agents/skills/quality-check/scripts/audit_repo.py`

## Architecture & Boundaries
1. **`intent.md` & `intents/` (Why & What)**: Check `intent.md` and `intents/*.md` before adding new features. Never violate the Anti-Goals defined in `intent.md`.
2. **`specs/` (How)**: Every non-trivial feature in `intents/` should have a corresponding technical contract in `specs/` before or alongside implementation.
3. **`src/core/` (Pure Domain Layer)**: Contains models and storage logic. See `src/core/AGENTS.md` for strict purity constraints.
4. **`src/cli.py` (Presentation Layer)**: Handles `argparse`, terminal formatting, `stdout`/`stderr`, and process exit codes.
5. **`tests/` (Verification Layer)**: Every new behavior or bug fix requires unit tests using `unittest` and `tempfile.TemporaryDirectory` (never touch the user's real `.taskpulse.json` in tests).

## Coding Style
- Use `dataclasses` and explicit type hints on all public functions and methods.
- Raise `ValueError` for invalid domain inputs in `src/core/` and catch/report them cleanly in `src/cli.py`.
- Keep functions small, deterministic, and documented with concise docstrings.
