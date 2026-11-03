"""Command-line interface for TaskPulse."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from src.core.models import VALID_PRIORITIES
from src.core.store import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskpulse",
        description="TaskPulse — Lightweight local sprint & task tracker.",
    )
    parser.add_argument(
        "--db",
        default=".taskpulse.json",
        help="Path to JSON task database (default: .taskpulse.json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task summary title")
    add_p.add_argument(
        "--priority",
        choices=VALID_PRIORITIES,
        default="medium",
        help="Task priority (default: medium)",
    )

    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument(
        "--status",
        choices=("all", "todo", "done"),
        default="all",
        help="Filter by task status (default: all)",
    )

    done_p = subparsers.add_parser("done", help="Mark a task as completed")
    done_p.add_argument("id", type=int, help="Numeric ID of the task")

    subparsers.add_parser("stats", help="Display task completion summary")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TaskStore(Path(args.db))

    try:
        if args.command == "add":
            task = store.add_task(title=args.title, priority=args.priority)
            print(f"[#{task.id}] Added: {task.title} (priority={task.priority})")
            return 0

        if args.command == "list":
            tasks = store.list_tasks(status=args.status)
            if not tasks:
                print("No tasks found.")
                return 0
            for t in tasks:
                check = "x" if t.status == "done" else " "
                print(f"[{check}] #{t.id:<3} ({t.priority:<6}) {t.title}")
            return 0

        if args.command == "done":
            task = store.complete_task(args.id)
            print(f"[#{task.id}] Completed: {task.title}")
            return 0

        if args.command == "stats":
            summary = store.stats()
            print(
                f"Total: {summary['total']} | "
                f"Todo: {summary['todo']} | "
                f"Done: {summary['done']} | "
                f"Completion: {summary['completion_rate']}%"
            )
            return 0
    except (ValueError, KeyError) as exc:
        msg = exc.args[0] if exc.args else str(exc)
        print(f"Error: {msg}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
