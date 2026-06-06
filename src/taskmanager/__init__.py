"""taskmanager package — a small Task Management API.

This file marks the folder as a Python "package" so other code can do
`from taskmanager import TaskManager`. We re-export the main pieces here
so users don't need to know which file they live in.
"""

from .models import Task, Status, Priority, TaskError
from .manager import TaskManager

__all__ = ["Task", "Status", "Priority", "TaskError", "TaskManager"]
