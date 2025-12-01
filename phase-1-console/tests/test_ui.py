"""Tests for the UI module."""

from datetime import datetime
from io import StringIO
from unittest.mock import patch

import pytest

from todo.models import Task
from todo.ui import (
    format_task_list,
    format_empty_list_message,
    display_task_created_message,
    display_toggle_message,
    display_update_success_message,
    display_delete_success_message,
    display_delete_cancelled_message,
    display_welcome_message,
    display_goodbye_message,
    display_error_message,
)


# =============================================================================
# User Story 1: View All Tasks (P1)
# =============================================================================


class TestFormatTaskList:
    """Tests for task list formatting (US1)."""

    def test_format_task_list_empty(self) -> None:
        """Test format_task_list returns empty message for empty list."""
        result = format_empty_list_message()

        assert "No tasks yet" in result
        assert "Add your first task" in result

    def test_format_task_list_with_tasks(self) -> None:
        """Test format_task_list formats tasks with ID, status, title, date."""
        tasks = [
            Task(id=1, title="Buy groceries", completed=False,
                 created_at=datetime(2025, 12, 1, 10, 30)),
            Task(id=2, title="Call dentist", completed=True,
                 created_at=datetime(2025, 12, 1, 9, 15)),
        ]

        result = format_task_list(tasks)

        # Check task 1 (pending)
        assert "1" in result
        assert "Buy groceries" in result
        assert "[ ]" in result  # Pending indicator

        # Check task 2 (completed)
        assert "2" in result
        assert "Call dentist" in result
        assert "[x]" in result  # Completed indicator


# =============================================================================
# User Story 2: Add New Task (P2)
# =============================================================================


class TestTaskCreatedMessage:
    """Tests for task creation confirmation messages (US2)."""

    def test_display_task_created_message(self) -> None:
        """Test that task created message shows task ID."""
        task = Task(id=1, title="Buy groceries")

        result = display_task_created_message(task)

        assert "1" in result
        assert "created" in result.lower()


# =============================================================================
# User Story 3: Mark Task Complete/Incomplete (P3)
# =============================================================================


class TestToggleMessage:
    """Tests for toggle completion messages (US3)."""

    def test_display_toggle_complete_message(self) -> None:
        """Test message for marking task complete."""
        task = Task(id=1, title="Buy groceries", completed=True)

        result = display_toggle_message(task)

        assert "complete" in result.lower()
        assert "Buy groceries" in result

    def test_display_toggle_incomplete_message(self) -> None:
        """Test message for marking task incomplete."""
        task = Task(id=1, title="Buy groceries", completed=False)

        result = display_toggle_message(task)

        assert "incomplete" in result.lower()


# =============================================================================
# User Story 4: Update Task (P4)
# =============================================================================


class TestUpdateMessage:
    """Tests for update task messages (US4)."""

    def test_display_update_success_message(self) -> None:
        """Test update success message shows task ID."""
        task = Task(id=1, title="Updated title")

        result = display_update_success_message(task)

        assert "1" in result
        assert "updated" in result.lower()


# =============================================================================
# User Story 5: Delete Task (P5)
# =============================================================================


class TestDeleteMessages:
    """Tests for delete task messages (US5)."""

    def test_display_delete_success_message(self) -> None:
        """Test delete success message."""
        result = display_delete_success_message()

        assert "deleted" in result.lower()

    def test_display_delete_cancelled_message(self) -> None:
        """Test delete cancelled message."""
        result = display_delete_cancelled_message()

        assert "cancelled" in result.lower()


# =============================================================================
# User Story 6: Navigate Menu and Exit (P6)
# =============================================================================


class TestMenuMessages:
    """Tests for menu and navigation messages (US6)."""

    def test_display_welcome_message(self) -> None:
        """Test welcome message."""
        result = display_welcome_message()

        assert "Welcome" in result or "welcome" in result.lower()

    def test_display_goodbye_message(self) -> None:
        """Test goodbye message includes data warning."""
        result = display_goodbye_message()

        assert "Goodbye" in result or "goodbye" in result.lower()
        assert "not saved" in result.lower() or "in-memory" in result.lower()

    def test_display_error_message(self) -> None:
        """Test error message formatting."""
        result = display_error_message("Something went wrong")

        assert "Something went wrong" in result
