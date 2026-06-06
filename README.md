# Phase-1-Task-Management-API

A small, clean task manager built with **standard-library Python**, laid out
the way real Python projects are. It demonstrates the Phase 1 Foundations
concepts: dataclasses, enums, type hints, OOP, custom exceptions, file
operations, comprehensions, and context managers.

## Project layout (industry standard)

```
Phase-1-Task-Management-API/
├── pyproject.toml        # project metadata, dependencies, tooling config
├── README.md             # you are here
├── .gitignore            # files git should ignore
├── src/
│   └── taskmanager/      # the actual package (importable code)
│       ├── __init__.py   # marks the folder as a package
│       ├── models.py     # Task dataclass, Status/Priority enums, exceptions
│       ├── manager.py    # TaskManager: create/update/delete/search + storage
│       └── cli.py        # interactive terminal menu
└── tests/
    └── test_manager.py   # automated tests (run with pytest)
```

Why `src/`? It keeps importable code in one obvious place and prevents a
whole class of "it worked on my machine" import bugs. It's the modern default.

## Setup (one time)

From the project folder, with the virtual environment active:

```
.venv\Scripts\activate
pip install -e ".[dev]"
```

`-e` ("editable") installs the package so `import taskmanager` works anywhere,
while still pointing at your source files so edits take effect immediately.
`[dev]` also installs pytest.

## Run the interactive app

```
taskmanager
```

(or `python -m taskmanager.cli`). Tasks are saved to `tasks.json`.

## Run the tests

```
pytest
```

## Use it as a library (the "API")

```python
from taskmanager import TaskManager, Priority, Status

tm = TaskManager("tasks.json")
t = tm.create_task("Learn Python", priority=Priority.HIGH, tags=["study"])
tm.update_task(t.id, status=Status.IN_PROGRESS)
print(tm.search(tag="study"))
tm.delete_task(t.id)
```

## The four required features

- **Create** → `create_task(title, description, priority, tags)`
- **Update** → `update_task(id, title=..., status=..., priority=..., tags=...)`
- **Delete** → `delete_task(id)`
- **Search** → `search(text=..., status=..., priority=..., tag=...)`
