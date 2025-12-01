# Contract: TaskManager Interface

**Feature**: 001-console-todo-app
**Date**: 2025-12-01
**Type**: Internal Python Interface (no REST API in Phase I)

## Overview

This document defines the public interface of the `TaskManager` class, which serves as the business logic layer between the UI and data storage.

## Class: TaskManager

### Constructor

```python
def __init__(self) -> None:
    """Initialize an empty task manager with ID counter starting at 1."""
```

### Methods

#### add_task

```python
def add_task(self, title: str, description: str = "") -> Task:
    """Create a new task and add it to the collection.

    Args:
        title: Task title (required, 1-200 characters).
        description: Task description (optional, max 1000 characters).

    Returns:
        The newly created Task with auto-generated ID.

    Raises:
        ValueError: If title is empty or exceeds 200 characters.
        ValueError: If description exceeds 1000 characters.
    """
```

#### get_all_tasks

```python
def get_all_tasks(self) -> list[Task]:
    """Return all tasks in the collection.

    Returns:
        List of all Task objects (may be empty).
    """
```

#### get_task

```python
def get_task(self, task_id: int) -> Task:
    """Retrieve a single task by ID.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        The Task with the specified ID.

    Raises:
        KeyError: If no task exists with the given ID.
    """
```

#### update_task

```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> Task:
    """Update an existing task's title and/or description.

    Args:
        task_id: The unique identifier of the task to update.
        title: New title (None to keep current). If provided, must be 1-200 chars.
        description: New description (None to keep current). Max 1000 chars.

    Returns:
        The updated Task object.

    Raises:
        KeyError: If no task exists with the given ID.
        ValueError: If new title is empty or exceeds 200 characters.
        ValueError: If new description exceeds 1000 characters.
    """
```

#### delete_task

```python
def delete_task(self, task_id: int) -> Task:
    """Remove a task from the collection.

    Args:
        task_id: The unique identifier of the task to delete.

    Returns:
        The deleted Task object (for confirmation message).

    Raises:
        KeyError: If no task exists with the given ID.
    """
```

#### toggle_complete

```python
def toggle_complete(self, task_id: int) -> Task:
    """Toggle the completion status of a task.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        The updated Task object with toggled status.

    Raises:
        KeyError: If no task exists with the given ID.
    """
```

#### has_tasks

```python
def has_tasks(self) -> bool:
    """Check if there are any tasks in the collection.

    Returns:
        True if at least one task exists, False otherwise.
    """
```

#### task_count

```python
def task_count(self) -> int:
    """Return the total number of tasks.

    Returns:
        Integer count of tasks in the collection.
    """
```

## Error Contract

### ValueError

Raised for validation failures:
- Empty title: `"Title is required"`
- Title too long: `"Title must be 200 characters or less"`
- Description too long: `"Description must be 1000 characters or less"`

### KeyError

Raised when task ID not found:
- Message format: `"Task with ID {id} not found"`

## Usage Example

```python
from todo.manager import TaskManager
from todo.models import Task

# Initialize
manager = TaskManager()

# Add tasks
task1 = manager.add_task("Buy groceries", "Get milk and eggs")
task2 = manager.add_task("Call dentist")

# View all
all_tasks = manager.get_all_tasks()  # [task1, task2]

# Toggle completion
manager.toggle_complete(task1.id)  # task1.completed = True

# Update
manager.update_task(task2.id, title="Call dentist office")

# Delete
deleted = manager.delete_task(task1.id)

# Check if empty
if not manager.has_tasks():
    print("No tasks yet!")
```

## Future Evolution

Phase II (Web App) will add:
- REST API endpoints wrapping these methods
- User context parameter for multi-user support
- Async versions for database operations

The interface design supports this evolution by:
- Keeping methods focused and single-purpose
- Using explicit exceptions for error handling
- Returning Task objects (serializable to JSON)
