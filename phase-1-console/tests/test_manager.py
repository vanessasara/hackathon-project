"""Tests for the TaskManager class."""

import pytest

from todo.manager import TaskManager
from todo.models import Task


class TestTaskManagerInitialization:
    """Tests for TaskManager initialization."""

    def test_task_manager_initialization(self) -> None:
        """Test that TaskManager initializes with empty task list."""
        manager = TaskManager()

        assert manager.get_all_tasks() == []
        assert manager.task_count() == 0


# =============================================================================
# User Story 1: View All Tasks (P1)
# =============================================================================


class TestGetAllTasks:
    """Tests for viewing all tasks (US1)."""

    def test_get_all_tasks_empty(self) -> None:
        """Test get_all_tasks returns empty list when no tasks exist."""
        manager = TaskManager()

        result = manager.get_all_tasks()

        assert result == []
        assert isinstance(result, list)

    def test_get_all_tasks_returns_list(self) -> None:
        """Test get_all_tasks returns list of tasks after adding."""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")

        result = manager.get_all_tasks()

        assert len(result) == 2
        assert all(isinstance(task, Task) for task in result)


class TestHasTasks:
    """Tests for checking if tasks exist (US1)."""

    def test_has_tasks_false_when_empty(self) -> None:
        """Test has_tasks returns False when no tasks exist."""
        manager = TaskManager()

        assert manager.has_tasks() is False

    def test_has_tasks_true_with_tasks(self) -> None:
        """Test has_tasks returns True when tasks exist."""
        manager = TaskManager()
        manager.add_task("Test task")

        assert manager.has_tasks() is True


# =============================================================================
# User Story 2: Add New Task (P2)
# =============================================================================


class TestAddTask:
    """Tests for adding tasks (US2)."""

    def test_add_task_returns_task_with_id(self) -> None:
        """Test add_task returns a Task with auto-generated ID."""
        manager = TaskManager()

        task = manager.add_task("Buy groceries")

        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Buy groceries"

    def test_add_task_sequential_ids(self) -> None:
        """Test that task IDs are sequential."""
        manager = TaskManager()

        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_description(self) -> None:
        """Test add_task with both title and description."""
        manager = TaskManager()

        task = manager.add_task("Meeting prep", "Prepare slides for Monday")

        assert task.title == "Meeting prep"
        assert task.description == "Prepare slides for Monday"

    def test_add_task_empty_title_raises_error(self) -> None:
        """Test add_task raises ValueError for empty title."""
        manager = TaskManager()

        with pytest.raises(ValueError) as exc_info:
            manager.add_task("")

        assert "Title is required" in str(exc_info.value)

    def test_add_task_whitespace_title_raises_error(self) -> None:
        """Test add_task raises ValueError for whitespace-only title."""
        manager = TaskManager()

        with pytest.raises(ValueError) as exc_info:
            manager.add_task("   ")

        assert "Title is required" in str(exc_info.value)

    def test_add_task_title_too_long_raises_error(self) -> None:
        """Test add_task raises ValueError for title > 200 characters."""
        manager = TaskManager()
        long_title = "x" * 201

        with pytest.raises(ValueError) as exc_info:
            manager.add_task(long_title)

        assert "200 characters" in str(exc_info.value)

    def test_add_task_description_too_long_raises_error(self) -> None:
        """Test add_task raises ValueError for description > 1000 characters."""
        manager = TaskManager()
        long_description = "x" * 1001

        with pytest.raises(ValueError) as exc_info:
            manager.add_task("Valid title", long_description)

        assert "1000 characters" in str(exc_info.value)


# =============================================================================
# User Story 3: Mark Task Complete/Incomplete (P3)
# =============================================================================


class TestToggleComplete:
    """Tests for toggling task completion status (US3)."""

    def test_toggle_complete_pending_to_completed(self) -> None:
        """Test toggle_complete changes pending task to completed."""
        manager = TaskManager()
        task = manager.add_task("Test task")
        assert task.completed is False

        result = manager.toggle_complete(task.id)

        assert result.completed is True
        assert result.id == task.id

    def test_toggle_complete_completed_to_pending(self) -> None:
        """Test toggle_complete changes completed task back to pending."""
        manager = TaskManager()
        task = manager.add_task("Test task")
        manager.toggle_complete(task.id)  # Make it completed
        assert task.completed is True

        result = manager.toggle_complete(task.id)

        assert result.completed is False

    def test_toggle_complete_not_found_raises_error(self) -> None:
        """Test toggle_complete raises KeyError for non-existent task."""
        manager = TaskManager()

        with pytest.raises(KeyError) as exc_info:
            manager.toggle_complete(999)

        assert "999" in str(exc_info.value)


# =============================================================================
# User Story 4: Update Task (P4)
# =============================================================================


class TestUpdateTask:
    """Tests for updating tasks (US4)."""

    def test_update_task_title(self) -> None:
        """Test update_task can update title."""
        manager = TaskManager()
        task = manager.add_task("Original title")

        result = manager.update_task(task.id, title="New title")

        assert result.title == "New title"

    def test_update_task_description(self) -> None:
        """Test update_task can update description."""
        manager = TaskManager()
        task = manager.add_task("Title", "Original description")

        result = manager.update_task(task.id, description="New description")

        assert result.description == "New description"
        assert result.title == "Title"  # Title unchanged

    def test_update_task_both_fields(self) -> None:
        """Test update_task can update both title and description."""
        manager = TaskManager()
        task = manager.add_task("Old title", "Old description")

        result = manager.update_task(task.id, title="New title", description="New desc")

        assert result.title == "New title"
        assert result.description == "New desc"

    def test_update_task_keep_original_if_none(self) -> None:
        """Test update_task keeps original values when None passed."""
        manager = TaskManager()
        task = manager.add_task("Original title", "Original desc")

        result = manager.update_task(task.id)  # No changes

        assert result.title == "Original title"
        assert result.description == "Original desc"

    def test_update_task_not_found_raises_error(self) -> None:
        """Test update_task raises KeyError for non-existent task."""
        manager = TaskManager()

        with pytest.raises(KeyError) as exc_info:
            manager.update_task(999, title="New title")

        assert "999" in str(exc_info.value)


# =============================================================================
# User Story 5: Delete Task (P5)
# =============================================================================


class TestDeleteTask:
    """Tests for deleting tasks (US5)."""

    def test_delete_task_removes_from_list(self) -> None:
        """Test delete_task removes task from the list."""
        manager = TaskManager()
        task = manager.add_task("Task to delete")
        assert manager.task_count() == 1

        manager.delete_task(task.id)

        assert manager.task_count() == 0

    def test_delete_task_returns_deleted_task(self) -> None:
        """Test delete_task returns the deleted task for confirmation."""
        manager = TaskManager()
        task = manager.add_task("Task to delete")

        result = manager.delete_task(task.id)

        assert result.id == task.id
        assert result.title == "Task to delete"

    def test_delete_task_not_found_raises_error(self) -> None:
        """Test delete_task raises KeyError for non-existent task."""
        manager = TaskManager()

        with pytest.raises(KeyError) as exc_info:
            manager.delete_task(999)

        assert "999" in str(exc_info.value)
