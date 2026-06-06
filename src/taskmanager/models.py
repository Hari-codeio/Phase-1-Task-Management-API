"""
models.py
=========
The DATA layer of our Task Management API.

Concepts from Phase 1 used here:
  - Enums        -> a fixed set of allowed values (status, priority)
  - Dataclasses  -> classes that mostly just hold data, with less boilerplate
  - Type hints   -> annotations like `title: str` that document intent
  - Exceptions   -> custom error types so callers can react precisely
"""

from __future__ import annotations  # lets us reference types before they're defined

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum


# ---------------------------------------------------------------------
# 1. ENUMS  -- a value can only be one of these named options.
# ---------------------------------------------------------------------
class Status(str, Enum):
    """The lifecycle of a task. Inheriting `str` makes it JSON-friendly."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(str, Enum):
    """How urgent a task is."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ---------------------------------------------------------------------
# 2. CUSTOM EXCEPTIONS  -- our own error types.
#    Catching `TaskError` catches all of ours; the subclasses are specific.
# ---------------------------------------------------------------------
class TaskError(Exception):
    """Base class for every error this app raises."""


class TaskNotFoundError(TaskError):
    """Raised when a task id doesn't exist."""


class ValidationError(TaskError):
    """Raised when task data is invalid (e.g. empty title)."""


# ---------------------------------------------------------------------
# 3. THE TASK DATACLASS  -- one to-do item.
# ---------------------------------------------------------------------
def _now() -> str:
    """Current UTC time as a readable ISO string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: Status = Status.TODO
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)   # each Task gets its OWN list
    created_at: str = field(default_factory=_now)

    def __post_init__(self) -> None:
        """Runs automatically right after the dataclass is created.
        We use it to validate the incoming data."""
        if not self.title or not self.title.strip():
            raise ValidationError("Task title cannot be empty.")
        # If someone passed plain strings (e.g. from JSON), coerce to enums.
        self.status = Status(self.status)
        self.priority = Priority(self.priority)

    # ----- serialization helpers (used for saving/loading JSON) -------
    def to_dict(self) -> dict:
        """Turn this Task into a plain dict (enums become their .value)."""
        data = asdict(self)
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Rebuild a Task from a plain dict (the reverse of to_dict)."""
        return cls(**data)
