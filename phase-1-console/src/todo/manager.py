"""Task manager business logic for the Todo application.

This module contains the TaskManager class that handles all CRUD operations
for tasks, including validation and error handling.
"""

from todo.models import Task


class TaskManager:
    """Manages a collection of tasks with CRUD operations.

    The TaskManager encapsulates all business logic for managing tasks,
    including adding, updating, deleting, and querying tasks. It maintains
    an in-memory list of tasks and handles ID generation.

    Attributes:
        _tasks: Internal list of Task objects.
        _next_id: Counter for generating sequential task IDs.
    """

    def __init__(self) -> None:
        """Initialize an empty task manager with ID counter starting at 1."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks in the collection.

        Returns:
            List of all Task objects (may be empty).
        """
        return list(self._tasks)

    def task_count(self) -> int:
        """Return the total number of tasks.

        Returns:
            Integer count of tasks in the collection.
        """
        return len(self._tasks)

    def has_tasks(self) -> bool:
        """Check if there are any tasks in the collection.

        Returns:
            True if at least one task exists, False otherwise.
        """
        return len(self._tasks) > 0

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
        # Validate title
        title = title.strip()
        if not title:
            raise ValueError("Title is required")
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

        # Validate description
        if len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        # Create and store task
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a single task by ID.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The Task with the specified ID.

        Raises:
            KeyError: If no task exists with the given ID.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"Task with ID {task_id} not found")

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle the completion status of a task.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The updated Task object with toggled status.

        Raises:
            KeyError: If no task exists with the given ID.
        """
        task = self.get_task(task_id)
        task.completed = not task.completed
        return task

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
        task = self.get_task(task_id)

        # Update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title is required")
            if len(title) > 200:
                raise ValueError("Title must be 200 characters or less")
            task.title = title

        # Update description if provided
        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> Task:
        """Remove a task from the collection.

        Args:
            task_id: The unique identifier of the task to delete.

        Returns:
            The deleted Task object (for confirmation message).

        Raises:
            KeyError: If no task exists with the given ID.
        """
        task = self.get_task(task_id)
        self._tasks.remove(task)
        return task
