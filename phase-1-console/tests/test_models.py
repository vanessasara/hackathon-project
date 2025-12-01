"""Tests for the Task model."""

from datetime import datetime

import pytest

from todo.models import Task


class TestTaskCreation:
    """Tests for Task creation and initialization."""

    def test_task_creation_with_required_fields(self) -> None:
        """Test that a Task can be created with required id and title."""
        task = Task(id=1, title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"

    def test_task_default_values(self) -> None:
        """Test that Task has correct default values for optional fields."""
        task = Task(id=1, title="Test task")

        assert task.description == ""
        assert task.completed is False
        assert isinstance(task.created_at, datetime)
