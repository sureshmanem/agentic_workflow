"""JSON-backed task persistence store."""
from __future__ import annotations

import json
from pathlib import Path

from src.core.models import Task, utc_now_iso


class TaskStore:
    """Manages reading, writing, and querying Task objects from a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def _load_raw(self) -> tuple[int, list[Task]]:
        if not self.path.exists():
            return 1, []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        tasks = [Task.from_dict(item) for item in raw.get("tasks", [])]
        default_next = (max((t.id for t in tasks), default=0) + 1)
        next_id = int(raw.get("next_id", default_next))
        return next_id, tasks

    def _save_raw(self, next_id: int, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "next_id": next_id,
            "tasks": [t.to_dict() for t in tasks],
        }
        self.path.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )

    def add_task(self, title: str, priority: str = "medium") -> Task:
        """Create and persist a new task."""
        next_id, tasks = self._load_raw()
        task = Task(id=next_id, title=title, priority=priority)
        tasks.append(task)
        self._save_raw(next_id + 1, tasks)
        return task

    def list_tasks(self, status: str = "all") -> list[Task]:
        """Return tasks filtered by status ('all', 'todo', or 'done')."""
        if status not in ("all", "todo", "done"):
            raise ValueError(f"Unsupported status filter: '{status}'")
        _, tasks = self._load_raw()
        if status == "all":
            return tasks
        return [t for t in tasks if t.status == status]

    def complete_task(self, task_id: int) -> Task:
        """Mark an existing task as done and persist the completion timestamp."""
        next_id, tasks = self._load_raw()
        for task in tasks:
            if task.id == task_id:
                task.status = "done"
                if task.completed_at is None:
                    task.completed_at = utc_now_iso()
                self._save_raw(next_id, tasks)
                return task
        raise KeyError(f"Task #{task_id} not found.")

    def stats(self) -> dict[str, int | float]:
        """Compute summary statistics across all tasks."""
        _, tasks = self._load_raw()
        total = len(tasks)
        done = sum(1 for t in tasks if t.status == "done")
        todo = total - done
        completion_rate = round((done / total) * 100.0, 1) if total > 0 else 0.0
        return {
            "total": total,
            "todo": todo,
            "done": done,
            "completion_rate": completion_rate,
        }
