# Intent 002: Priority Filtering & Overdue Task Summary

## 1. Background & Motivation ("The Why")
As a task list grows beyond 10-15 items, `python3 -m src.cli list` shows everything at once without letting developers focus on urgent (`high` priority) or overdue items.

## 2. Core Objectives ("The What")
- Allow filtering `list` output by `--priority {low,medium,high}`.
- Support an optional `--due YYYY-MM-DD` date field when adding a task (`add` command).
- Include an `overdue` count in `stats` output comparing incomplete task due dates against today's ISO date.

## 3. Guardrails & Anti-Goals ("What NOT to Build")
- Do NOT use third-party date parsers (`python-dateutil`, `pendulum`); use `datetime.date.fromisoformat` from the Python standard library.
- Existing `.taskpulse.json` files without a `due_date` field must continue loading cleanly (`due_date: Optional[str] = None`).
- Do NOT break existing CLI flags or output semantics.

## 4. Success Criteria
1. `python3 -m src.cli add "Fix auth bug" --priority high --due 2026-11-10` stores `due_date`.
2. `python3 -m src.cli list --priority high` returns only `high` priority tasks.
3. Unit tests cover backward compatibility, invalid ISO dates, `--priority` filtering, and `overdue` stats.
