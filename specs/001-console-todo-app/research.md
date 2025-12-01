# Research: Console Todo App

**Feature**: 001-console-todo-app
**Date**: 2025-12-01
**Purpose**: Resolve technical decisions and best practices for Phase I implementation

## Research Tasks

### 1. Python Dataclass Best Practices

**Decision**: Use `@dataclass` decorator from Python's standard library

**Rationale**:
- Built into Python 3.7+ (no external dependency)
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Supports type hints natively
- `field()` function for default factories (e.g., `datetime.now()`)
- Frozen option available for immutability if needed later

**Alternatives Considered**:
- `NamedTuple`: Rejected - immutable by default, less flexible for mutable Task state
- `Pydantic`: Rejected - external dependency, overkill for Phase I
- Plain class: Rejected - more boilerplate, violates DRY principle

**Implementation Pattern**:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

### 2. In-Memory Storage Pattern

**Decision**: Use a Python list managed by TaskManager class

**Rationale**:
- Simple and sufficient for Phase I requirements
- O(n) lookup by ID is acceptable for ~100 tasks
- TaskManager encapsulates storage details (Constitution Principle V)
- Easy to swap for database in future phases

**Alternatives Considered**:
- Dictionary keyed by ID: Considered - O(1) lookup but list maintains insertion order naturally
- SQLite in-memory: Rejected - external complexity, violates Phase I constraints
- Singleton pattern: Rejected - unnecessary complexity for single-user app

**Implementation Pattern**:
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

### 3. Input Validation Strategy

**Decision**: Validate at UI boundary, raise exceptions from manager for business rules

**Rationale**:
- UI handles user-facing validation messages
- Manager enforces business rules (title length, existence checks)
- Separation of concerns per Constitution Principle IV
- Exceptions provide clear error handling path

**Alternatives Considered**:
- Return tuples (success, result/error): Rejected - less Pythonic, harder to compose
- Validation decorators: Rejected - over-engineering for Phase I
- All validation in UI: Rejected - duplicates logic if adding API later

**Error Types**:
- `ValueError`: Invalid input format (empty title, too long)
- `KeyError` or custom `TaskNotFoundError`: Task ID doesn't exist

### 4. Console Menu Interface Pattern

**Decision**: While loop with numbered menu, input() for user interaction

**Rationale**:
- Standard Python input/output (no external dependencies)
- Clear, predictable flow per Constitution Principle VI
- Easy to test with mocked input/output

**Alternatives Considered**:
- `curses` library: Rejected - platform-specific, complex
- `click` CLI framework: Rejected - external dependency, more suited for command args
- `prompt_toolkit`: Rejected - external dependency, overkill for simple menu

**Implementation Pattern**:
```python
def display_menu() -> None:
    print("\n=== Todo Manager ===")
    print("1. View all tasks")
    print("2. Add new task")
    print("3. Mark task as complete/incomplete")
    print("4. Update task")
    print("5. Delete task")
    print("6. Exit")

def get_menu_choice() -> int:
    while True:
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("Invalid choice. Please enter a number between 1 and 6")
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 6")
```

### 5. Graceful Exit Handling (Ctrl+C)

**Decision**: Use try/except KeyboardInterrupt in main loop

**Rationale**:
- Standard Python pattern for handling Ctrl+C
- Provides clean exit message per spec edge case
- No external dependencies

**Implementation Pattern**:
```python
def main() -> None:
    manager = TaskManager()
    try:
        while True:
            display_menu()
            choice = get_menu_choice()
            # ... handle choice
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
```

### 6. Testing Strategy

**Decision**: pytest with fixture-based test organization

**Rationale**:
- pytest is mandated by Constitution
- Fixtures provide clean test setup
- Parameterized tests for edge cases
- Mock input/output for UI tests

**Test Categories**:
1. **Unit tests (test_models.py)**: Task creation, default values, field validation
2. **Unit tests (test_manager.py)**: CRUD operations, ID generation, not-found handling
3. **Integration tests (test_ui.py)**: Menu flow, input validation, output formatting

**Implementation Pattern**:
```python
import pytest
from todo.manager import TaskManager

@pytest.fixture
def manager() -> TaskManager:
    return TaskManager()

def test_add_task_returns_task_with_id(manager: TaskManager) -> None:
    task = manager.add_task("Buy groceries")
    assert task.id == 1
    assert task.title == "Buy groceries"
```

## Summary

All technical decisions align with Constitution principles:
- Standard library only (no external dependencies except pytest)
- Clear separation: models.py, manager.py, ui.py, main.py
- TDD-friendly structure with testable components
- Abstracted storage for future evolution

No NEEDS CLARIFICATION items remain. Ready for Phase 1 design.
