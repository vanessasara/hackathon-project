# Todo Manager - Phase 1 Console App

An in-memory console-based todo list manager built with Python.

## Features

- **View all tasks**: Display tasks with ID, status, title, and creation date
- **Add new task**: Create tasks with title (required) and optional description
- **Mark complete/incomplete**: Toggle task completion status
- **Update task**: Modify task title and/or description
- **Delete task**: Remove tasks with confirmation prompt

## Requirements

- Python 3.13+
- [UV](https://docs.astral.sh/uv/) package manager

## Setup

1. **Navigate to the phase-1-console directory**:
   ```bash
   cd phase-1-console
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run tests** (TDD verification):
   ```bash
   uv run pytest
   ```

## Usage

**Run the application**:
```bash
uv run python -m todo.main
```

Or using the entry point:
```bash
uv run todo
```

### Menu Options

```
=== Todo Manager ===
1. View all tasks
2. Add new task
3. Mark task as complete/incomplete
4. Update task
5. Delete task
6. Exit
```

### Example Session

```
Welcome to Todo Manager!

=== Todo Manager ===
1. View all tasks
2. Add new task
3. Mark task as complete/incomplete
4. Update task
5. Delete task
6. Exit

Enter your choice (1-6): 2
Enter task title: Buy groceries
Enter description (optional): Get milk and eggs
✓ Task created with ID: 1

Enter your choice (1-6): 1

=== Your Tasks ===

ID  Status  Title                          Created
------------------------------------------------------------
1   [ ]     Buy groceries                  2025-12-01 20:45

Total: 1 tasks (1 pending, 0 completed)

Enter your choice (1-6): 3
Enter task ID: 1
Task 'Buy groceries' marked as complete!

Enter your choice (1-6): 6
Goodbye! Your tasks are not saved (in-memory only).
```

## Project Structure

```
phase-1-console/
├── pyproject.toml       # Project configuration
├── README.md            # This file
├── src/
│   └── todo/
│       ├── __init__.py  # Package init
│       ├── main.py      # Entry point and main loop
│       ├── models.py    # Task dataclass
│       ├── manager.py   # Business logic (CRUD)
│       └── ui.py        # Menu and display functions
└── tests/
    ├── __init__.py
    ├── test_models.py   # Task model tests
    ├── test_manager.py  # TaskManager tests
    └── test_ui.py       # UI function tests
```

## Architecture

- **models.py**: Data structures (`Task` dataclass)
- **manager.py**: Business logic (`TaskManager` class)
- **ui.py**: User interface functions (display, prompts)
- **main.py**: Application entry point and menu dispatch

This separation follows the Single Responsibility Principle and enables independent testing.

## Keyboard Shortcuts

- `Ctrl+C`: Exit application gracefully at any prompt

## Limitations

- **In-memory only**: Tasks are NOT persisted. All data is lost when the application exits.
- **Single user**: No concurrent access support.
- **No pagination**: All tasks displayed at once.

## Development

This project was built using Spec-Driven Development (SDD) with Claude Code.

### Run Tests

```bash
uv run pytest -v
```

### Test Coverage

- 36 unit tests covering all user stories
- TDD (Test-Driven Development) methodology
- Tests for models, manager, and UI components

## License

Part of the Evolution of Todo hackathon project.
