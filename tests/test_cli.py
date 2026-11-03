"""Integration tests for the TaskPulse CLI."""
from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from src.cli import run


class TestCLI(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self._tmp.name) / "cli_tasks.json")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _invoke(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = run(["--db", self.db, *args])
        return code, out.getvalue(), err.getvalue()

    def test_full_cli_lifecycle(self) -> None:
        code, out, _ = self._invoke("list")
        self.assertEqual(code, 0)
        self.assertIn("No tasks found.", out)

        code, out, _ = self._invoke("add", "Test SKILL.md workflow", "--priority", "high")
        self.assertEqual(code, 0)
        self.assertIn("[#1] Added: Test SKILL.md workflow (priority=high)", out)

        code, out, _ = self._invoke("done", "1")
        self.assertEqual(code, 0)
        self.assertIn("[#1] Completed: Test SKILL.md workflow", out)

        code, out, _ = self._invoke("stats")
        self.assertEqual(code, 0)
        self.assertIn("Completion: 100.0%", out)

    def test_missing_task_returns_error_exit_code(self) -> None:
        code, _, err = self._invoke("done", "42")
        self.assertEqual(code, 1)
        self.assertIn("Task #42 not found.", err)


if __name__ == "__main__":
    unittest.main()
