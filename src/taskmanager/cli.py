"""
cli.py
======
The PRESENTATION layer -- a simple text menu you drive from the terminal.

RUN IT (after `pip install -e .`):
    taskmanager
or:
    python -m taskmanager.cli

Concepts from Phase 1 used here:
  - Functions (each menu action is its own function)
  - Loops (the main menu loops until you quit)
  - Conditionals (routing your choice)
  - Exception handling (we catch TaskError and show a friendly message)
  - input() / print() for interaction
"""

from .manager import TaskManager
from .models import Status, Priority, TaskError


# ---------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------
def show_task(task) -> None:
    """Pretty-print a single task on one line."""
    tags = f" [{', '.join(task.tags)}]" if task.tags else ""
    print(
        f"  #{task.id:<3} {task.title:<25} "
        f"{task.status.value:<12} {task.priority.value:<7}{tags}"
    )


def show_tasks(tasks) -> None:
    """Print a list of tasks, or a message if empty."""
    if not tasks:
        print("  (no tasks)")
        return
    for t in tasks:
        show_task(t)


def ask(prompt: str) -> str:
    """Ask the user something and trim the whitespace off their answer."""
    return input(prompt).strip()


# ---------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------
def do_create(tm: TaskManager) -> None:
    title = ask("Title: ")
    description = ask("Description (optional): ")
    pr = ask("Priority [low/medium/high] (default medium): ") or "medium"
    raw_tags = ask("Tags (comma separated, optional): ")
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    task = tm.create_task(
        title=title,
        description=description,
        priority=Priority(pr),
        tags=tags,
    )
    print(f"Created task #{task.id}.")


def do_list(tm: TaskManager) -> None:
    print("All tasks:")
    show_tasks(tm.list_all())


def do_update(tm: TaskManager) -> None:
    task_id = int(ask("Task id to update: "))
    print("Leave a field blank to keep it unchanged.")
    title = ask("New title: ") or None
    status = ask("New status [todo/in_progress/done]: ") or None
    priority = ask("New priority [low/medium/high]: ") or None

    task = tm.update_task(
        task_id,
        title=title,
        status=Status(status) if status else None,
        priority=Priority(priority) if priority else None,
    )
    print(f"Updated task #{task.id}.")


def do_delete(tm: TaskManager) -> None:
    task_id = int(ask("Task id to delete: "))
    task = tm.delete_task(task_id)
    print(f"Deleted task #{task.id} ('{task.title}').")


def do_search(tm: TaskManager) -> None:
    text = ask("Search text (optional): ") or None
    status = ask("Filter status [todo/in_progress/done] (optional): ") or None
    tag = ask("Filter tag (optional): ") or None

    results = tm.search(
        text=text,
        status=Status(status) if status else None,
        tag=tag,
    )
    print(f"Found {len(results)} task(s):")
    show_tasks(results)


# ---------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------
MENU = """
==================  TASK MANAGER  ==================
  1) Create task
  2) List tasks
  3) Update task
  4) Delete task
  5) Search tasks
  q) Quit
====================================================
"""

ACTIONS = {
    "1": do_create,
    "2": do_list,
    "3": do_update,
    "4": do_delete,
    "5": do_search,
}


def main() -> None:
    # Using the context manager guarantees a final save on exit.
    with TaskManager("tasks.json") as tm:
        while True:
            print(MENU)
            choice = ask("Choose an option: ")

            if choice.lower() == "q":
                print("Goodbye! Your tasks are saved in tasks.json.")
                break

            action = ACTIONS.get(choice)
            if action is None:
                print("Unknown option, try again.")
                continue

            # Catch our app's errors so one bad input doesn't crash the program.
            try:
                action(tm)
            except TaskError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
