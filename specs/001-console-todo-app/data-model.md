# Data Model: Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-01
**Source**: spec.md Key Entities section

## Entities

### Task

Represents a todo item in the application.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-generated | Positive integer, sequential starting from 1, unique | Unique identifier for the task |
| `title` | `str` | Yes | None | 1-200 characters, non-empty | Short description of what needs to be done |
| `description` | `str` | No | `""` (empty string) | Max 1000 characters | Detailed information about the task |
| `completed` | `bool` | No | `False` | Boolean | Whether the task is done |
| `created_at` | `datetime` | Yes | Auto-set on creation | Valid datetime | When the task was created |

### Python Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a todo item with title, description, and completion status.

    Attributes:
        id: Unique identifier (auto-generated positive integer).
        title: Short description of the task (1-200 characters, required).
        description: Detailed information (optional, max 1000 characters).
        completed: Whether the task is done (default: False).
        created_at: Timestamp when task was created (auto-set).
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

## Validation Rules

### Title Validation

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Required | `title.strip() == ""` | "Title is required" |
| Max Length | `len(title) > 200` | "Title must be 200 characters or less" |

### Description Validation

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Max Length | `len(description) > 1000` | "Description must be 1000 characters or less" |

### ID Validation (for operations)

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Valid Format | Non-integer input | "Please enter a valid task ID (number)" |
| Exists | ID not found in task list | "Task with ID {id} not found" |

## State Transitions

### Task Completion Status

```
┌─────────────┐                    ┌─────────────┐
│   Pending   │ ──── Toggle ─────▶ │  Completed  │
│ (completed  │                    │ (completed  │
│  = False)   │ ◀──── Toggle ───── │  = True)    │
└─────────────┘                    └─────────────┘
```

### Task Lifecycle

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│   Create   │ ───▶ │   Active   │ ───▶ │  Deleted   │
│  (add_task)│      │  (in list) │      │ (removed)  │
└────────────┘      └────────────┘      └────────────┘
                          │
                          ▼
                    ┌────────────┐
                    │   Update   │
                    │(title/desc)│
                    └────────────┘
```

## Relationships

Phase I has a single entity (Task) with no relationships to other entities.

**Future Phases Note**: When adding user accounts (Phase II+), Task will have a foreign key relationship to User. The current design's use of TaskManager abstraction supports this evolution.

## ID Generation Strategy

- Sequential integers starting from 1
- Incremented for each new task
- IDs are NOT reused after deletion (gaps acceptable per spec)
- Counter maintained in TaskManager instance

```python
class TaskManager:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task
```

## Display Format

### Task List View

```
ID  Status  Title                Created
──────────────────────────────────────────────
1   [ ]     Buy groceries        2025-12-01 10:30
2   [x]     Call dentist         2025-12-01 09:15
3   [ ]     Finish report        2025-12-01 14:45
```

### Single Task View (for update/delete confirmation)

```
Task #1: Buy groceries
Description: Get milk, eggs, and bread
Status: Pending
Created: 2025-12-01 10:30
```
