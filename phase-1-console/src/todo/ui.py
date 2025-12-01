"""User interface module for the Todo application.

This module contains functions for displaying menus, formatting output,
and handling user input for the console interface.
"""

from todo.models import Task


def format_empty_list_message() -> str:
    """Return a message for when the task list is empty.

    Returns:
        A friendly message encouraging users to add their first task.
    """
    return "No tasks yet. Add your first task!"


def format_task_list(tasks: list[Task]) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of Task objects to format.

    Returns:
        Formatted string with task details including ID, status, title, and date.
    """
    if not tasks:
        return format_empty_list_message()

    lines = []
    lines.append("")
    lines.append("=== Your Tasks ===")
    lines.append("")
    lines.append("ID  Status  Title                          Created")
    lines.append("-" * 60)

    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        title = task.title[:30] if len(task.title) > 30 else task.title
        date_str = task.created_at.strftime("%Y-%m-%d %H:%M")
        lines.append(f"{task.id:<3} {status}     {title:<30} {date_str}")

    # Summary
    completed = sum(1 for t in tasks if t.completed)
    pending = len(tasks) - completed
    lines.append("")
    lines.append(f"Total: {len(tasks)} tasks ({pending} pending, {completed} completed)")

    return "\n".join(lines)


def display_task_created_message(task: Task) -> str:
    """Return a confirmation message for a newly created task.

    Args:
        task: The newly created Task object.

    Returns:
        A confirmation message with the task ID.
    """
    return f"✓ Task created with ID: {task.id}"


def prompt_for_title() -> str:
    """Prompt the user to enter a task title.

    Returns:
        The title entered by the user (may be empty).
    """
    return input("Enter task title: ")


def prompt_for_description() -> str:
    """Prompt the user to enter an optional task description.

    Returns:
        The description entered by the user (may be empty).
    """
    return input("Enter description (optional): ")


# =============================================================================
# User Story 3: Mark Task Complete/Incomplete (P3)
# =============================================================================


def prompt_for_task_id() -> str:
    """Prompt the user to enter a task ID.

    Returns:
        The task ID string entered by the user.
    """
    return input("Enter task ID: ")


def display_toggle_message(task: Task) -> str:
    """Return a message for toggled task completion status.

    Args:
        task: The task whose status was toggled.

    Returns:
        A confirmation message with the new status.
    """
    status = "complete" if task.completed else "incomplete"
    return f"Task '{task.title}' marked as {status}!"


# =============================================================================
# User Story 4: Update Task (P4)
# =============================================================================


def prompt_for_new_title(current_title: str) -> str:
    """Prompt for a new title, showing the current one.

    Args:
        current_title: The current title of the task.

    Returns:
        The new title, or empty string to keep current.
    """
    return input(f"Enter new title (press Enter to keep '{current_title}'): ")


def prompt_for_new_description(current_description: str) -> str:
    """Prompt for a new description, showing the current one.

    Args:
        current_description: The current description of the task.

    Returns:
        The new description, or empty string to keep current.
    """
    current = current_description if current_description else "(none)"
    return input(f"Enter new description (press Enter to keep '{current}'): ")


def display_update_success_message(task: Task) -> str:
    """Return a success message for task update.

    Args:
        task: The updated task.

    Returns:
        A confirmation message.
    """
    return f"Task {task.id} updated successfully!"


# =============================================================================
# User Story 5: Delete Task (P5)
# =============================================================================


def prompt_delete_confirmation(task: Task) -> str:
    """Prompt for confirmation before deleting a task.

    Args:
        task: The task to be deleted.

    Returns:
        The user's response (y/n).
    """
    return input(f"Are you sure you want to delete '{task.title}'? (y/n): ")


def display_delete_success_message() -> str:
    """Return a success message for task deletion.

    Returns:
        A confirmation message.
    """
    return "Task deleted successfully"


def display_delete_cancelled_message() -> str:
    """Return a message when deletion is cancelled.

    Returns:
        A cancellation message.
    """
    return "Deletion cancelled"


# =============================================================================
# User Story 6: Navigate Menu and Exit (P6)
# =============================================================================


def display_welcome_message() -> str:
    """Return a welcome message for the application.

    Returns:
        The welcome message string.
    """
    return "Welcome to Todo Manager!"


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo Manager ===")
    print("1. View all tasks")
    print("2. Add new task")
    print("3. Mark task as complete/incomplete")
    print("4. Update task")
    print("5. Delete task")
    print("6. Exit")


def get_menu_choice() -> int:
    """Get and validate the user's menu choice.

    Returns:
        The valid menu choice (1-6).

    Note:
        Continues prompting until a valid choice is entered.
    """
    while True:
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            print("Invalid choice. Please enter a number between 1 and 6")
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 6")


def display_goodbye_message() -> str:
    """Return a goodbye message with data warning.

    Returns:
        The goodbye message with in-memory warning.
    """
    return "Goodbye! Your tasks are not saved (in-memory only)."


def display_error_message(message: str) -> str:
    """Return a formatted error message.

    Args:
        message: The error message to display.

    Returns:
        The formatted error message.
    """
    return f"Error: {message}"


def display_no_tasks_message() -> str:
    """Return a message when trying to operate on empty task list.

    Returns:
        A message indicating no tasks are available.
    """
    return "No tasks available"
