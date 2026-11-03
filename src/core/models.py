"""Domain models and validation for TaskPulse."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("todo", "done")


def utc_now_iso() -> str:
    """Return the current UTC timestamp as an ISO-8601 string."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Task:
    """Represents a single tracked engineering task."""

    id: int
    title: str
    priority: str = "medium"
    status: str = "todo"
    created_at: str = ""
    completed_at: str | None = None

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Task title cannot be empty.")
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{self.priority}'. Expected one of {VALID_PRIORITIES}."
            )
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{self.status}'. Expected one of {VALID_STATUSES}."
            )
        if not self.created_at:
            self.created_at = utc_now_iso()

    def to_dict(self) -> dict[str, object]:
        """Serialize the task to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Task:
        """Deserialize a task from a persisted JSON dictionary."""
        return cls(
            id=int(data["id"]),  # type: ignore[arg-type]
            title=str(data["title"]),
            priority=str(data.get("priority", "medium")),
            status=str(data.get("status", "todo")),
            created_at=str(data.get("created_at", "")),
            completed_at=(
                str(data["completed_at"])
                if data.get("completed_at") is not None
                else None
            ),
        )
