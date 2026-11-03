"""Unit tests for pure domain models and TaskStore."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.core.models import Task
from src.core.store import TaskStore


class TestTaskStore(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self._tmp.name) / "tasks.json"
        self.store = TaskStore(self.db_path)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_add_and_list_tasks(self) -> None:
        t1 = self.store.add_task("Read AGENTS.md", priority="high")
        t2 = self.store.add_task("Create first SKILL.md", priority="low")

        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)
        self.assertEqual(len(self.store.list_tasks()), 2)

    def test_complete_task_and_stats(self) -> None:
        self.store.add_task("Write intent.md")
        self.store.add_task("Implement CLI")
        done_task = self.store.complete_task(1)

        self.assertEqual(done_task.status, "done")
        self.assertIsNotNone(done_task.completed_at)

        todo_only = self.store.list_tasks(status="todo")
        self.assertEqual(len(todo_only), 1)
        self.assertEqual(todo_only[0].id, 2)

        stats = self.store.stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["done"], 1)
        self.assertEqual(stats["completion_rate"], 50.0)

    def test_validation_errors(self) -> None:
        with self.assertRaises(ValueError):
            Task(id=1, title="   ")
        with self.assertRaises(ValueError):
            Task(id=1, title="Valid", priority="urgent")
        with self.assertRaises(KeyError):
            self.store.complete_task(999)


if __name__ == "__main__":
    unittest.main()
