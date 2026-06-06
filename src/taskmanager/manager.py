"""
manager.py
==========
The LOGIC layer -- the actual "API" of the Task Management app.

`TaskManager` is the one class you talk to. It can:
    create_task, get_task, update_task, delete_task, search, list_all
and it persists everything to a JSON file (File Operations).

Concepts from Phase 1 used here:
  - OOP (a class with state + methods)
  - Type hints on every method
  - Exception handling (raising our custom errors)
  - File operations (reading/writing JSON)
  - Dict / list / comprehensions for searching
  - Context manager support (`with TaskManager(...) as tm:`)
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import (
    Task,
    Status,
    Priority,
    TaskNotFoundError,
)


class TaskManager:
    def __init__(self, storage_path: str | Path = "tasks.json") -> None:
        self.storage_path = Path(storage_path)
        self._tasks: dict[int, Task] = {}   # id -> Task
        self._next_id: int = 1
        self.load()                          # pull existing tasks off disk

    # ================================================================
    #  CREATE
    # ================================================================
    def create_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        tags: list[str] | None = None,
    ) -> Task:
        """Create a new task, store it, and return it."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
        )
        self._tasks[task.id] = task
        self._next_id += 1
        self.save()
        return task

    # ================================================================
    #  READ
    # ================================================================
    def get_task(self, task_id: int) -> Task:
        """Return one task, or raise TaskNotFoundError."""
        try:
            return self._tasks[task_id]
        except KeyError:
            raise TaskNotFoundError(f"No task with id {task_id}.") from None

    def list_all(self) -> list[Task]:
        """Return every task, sorted by id."""
        return [self._tasks[i] for i in sorted(self._tasks)]

    # ================================================================
    #  UPDATE
    # ================================================================
    def update_task(
        self,
        task_id: int,
        *,                              # everything after * must be passed by name
        title: str | None = None,
        description: str | None = None,
        status: Status | None = None,
        priority: Priority | None = None,
        tags: list[str] | None = None,
    ) -> Task:
        """Update only the fields you pass; leave the rest untouched."""
        task = self.get_task(task_id)   # raises if missing

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = Status(status)
        if priority is not None:
            task.priority = Priority(priority)
        if tags is not None:
            task.tags = tags

        self.save()
        return task

    # ================================================================
    #  DELETE
    # ================================================================
    def delete_task(self, task_id: int) -> Task:
        """Remove a task and return it. Raises if it doesn't exist."""
        task = self.get_task(task_id)
        del self._tasks[task_id]
        self.save()
        return task

    # ================================================================
    #  SEARCH  -- filter by free text, status, priority, or tag.
    # ================================================================
    def search(
        self,
        text: str | None = None,
        status: Status | None = None,
        priority: Priority | None = None,
        tag: str | None = None,
    ) -> list[Task]:
        """Return all tasks matching EVERY filter you provide."""
        results = self.list_all()

        if text:
            needle = text.lower()
            results = [
                t for t in results
                if needle in t.title.lower() or needle in t.description.lower()
            ]
        if status is not None:
            results = [t for t in results if t.status == Status(status)]
        if priority is not None:
            results = [t for t in results if t.priority == Priority(priority)]
        if tag:
            results = [t for t in results if tag in t.tags]

        return results

    # ================================================================
    #  PERSISTENCE  -- File Operations + JSON
    # ================================================================
    def save(self) -> None:
        """Write all tasks to the JSON file."""
        payload = {
            "next_id": self._next_id,
            "tasks": [t.to_dict() for t in self.list_all()],
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def load(self) -> None:
        """Read tasks from the JSON file if it exists."""
        if not self.storage_path.exists():
            return
        with open(self.storage_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        self._next_id = payload.get("next_id", 1)
        self._tasks = {
            d["id"]: Task.from_dict(d) for d in payload.get("tasks", [])
        }

    # ----- context manager: `with TaskManager() as tm:` --------------
    def __enter__(self) -> "TaskManager":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.save()
