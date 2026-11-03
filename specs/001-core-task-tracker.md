# Spec 001: Core TaskPulse CLI & Domain Store

- **Source Intent**: [intent.md](../intent.md)
- **Status**: Implemented

## 1. Data Model (`src/core/models.py`)
`Task` dataclass fields:
- `id` (`int`): Monotonically increasing integer starting at `1`.
- `title` (`str`): Non-empty trimmed string.
- `priority` (`str`): One of `"low"`, `"medium"`, `"high"` (default `"medium"`).
- `status` (`str`): One of `"todo"`, `"done"` (default `"todo"`).
- `created_at` (`str`): UTC ISO-8601 timestamp.
- `completed_at` (`Optional[str]`): UTC ISO-8601 timestamp or `None`.

## 2. Storage Contract (`src/core/store.py`)
`TaskStore(path: Path)` persists JSON with structure:
```json
{
  "next_id": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Learn AGENTS.md and SKILL.md",
      "priority": "high",
      "status": "todo",
      "created_at": "2026-11-02T22:00:00+00:00",
      "completed_at": null
    }
  ]
}
```

## 3. CLI Interface (`src/cli.py`)
Global option: `--db <path>` (defaults to `.taskpulse.json`).
Subcommands:
- `add <title> [--priority {low,medium,high}]` -> Creates task and prints `[#<id>] Added: <title> (priority=<priority>)`.
- `list [--status {all,todo,done}]` -> Prints formatted task rows or `No tasks found.`.
- `done <id>` -> Marks task `#<id>` as `"done"` and prints `[#<id>] Completed: <title>`. Raises exit code `1` if `<id>` does not exist.
- `stats` -> Prints total, todo, done, and completion rate percentage.

## 4. Verification
- `python3 -m unittest discover -s tests -v`
- `python3 .agents/skills/quality-check/scripts/audit_repo.py`
