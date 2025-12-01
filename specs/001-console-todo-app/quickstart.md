# Quickstart: Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-01
**Purpose**: Developer setup and usage guide

## Prerequisites

- Python 3.13 or higher
- UV package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

## Setup

### 1. Navigate to Phase 1 Directory

```bash
cd phase-1-console
```

### 2. Install Dependencies

```bash
uv sync
```

This installs the project in development mode with pytest for testing.

### 3. Run Tests (TDD Verification)

```bash
uv run pytest
```

All tests should pass before running the application.

### 4. Run the Application

```bash
uv run python -m todo.main
```

Or using the entry point (once configured in pyproject.toml):

```bash
uv run todo
```

## Usage

### Main Menu

When you start the application, you'll see:

```
=== Todo Manager ===
1. View all tasks
2. Add new task
3. Mark task as complete/incomplete
4. Update task
5. Delete task
6. Exit

Enter your choice (1-6):
```

### Adding a Task

1. Select option `2` from the menu
2. Enter the task title (required, 1-200 characters)
3. Enter the description (optional, press Enter to skip)
4. Confirmation message shows the new task ID

Example:
```
Enter task title: Buy groceries
Enter description (optional): Get milk and eggs

✓ Task created with ID: 1
```

### Viewing Tasks

Select option `1` to see all tasks:

```
=== Your Tasks ===

ID  Status  Title                Created
──────────────────────────────────────────────
1   [ ]     Buy groceries        2025-12-01 10:30
2   [x]     Call dentist         2025-12-01 09:15

Total: 2 tasks (1 pending, 1 completed)
```

### Marking Complete/Incomplete

1. Select option `3`
2. Enter the task ID
3. Status toggles between pending and completed

### Updating a Task

1. Select option `4`
2. Enter the task ID
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

### Deleting a Task

1. Select option `5`
2. Enter the task ID
3. Confirm with `y` or cancel with `n`

### Exiting

Select option `6` to exit. You'll see a reminder that tasks are not persisted:

```
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
│       ├── main.py      # Entry point
│       ├── models.py    # Task dataclass
│       ├── manager.py   # Business logic
│       └── ui.py        # Menu interface
└── tests/
    ├── __init__.py
    ├── test_models.py   # Model tests
    ├── test_manager.py  # Manager tests
    └── test_ui.py       # UI tests
```

## Development Workflow

Per Constitution Principle III (Test-First Development):

1. **Red**: Write a failing test
2. **Green**: Implement minimal code to pass
3. **Refactor**: Clean up while keeping tests green

Example TDD cycle:

```bash
# Write test first
uv run pytest tests/test_manager.py::test_add_task -v

# Implement to pass
# ... edit src/todo/manager.py ...

# Verify green
uv run pytest tests/test_manager.py::test_add_task -v

# Run all tests
uv run pytest
```

## Keyboard Shortcuts

- `Ctrl+C`: Exit application gracefully at any prompt

## Troubleshooting

### "Command not found: uv"

Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "No module named 'todo'"

Ensure you're in the `phase-1-console` directory and have run `uv sync`.

### Tests failing

Run with verbose output to see details:
```bash
uv run pytest -v
```
