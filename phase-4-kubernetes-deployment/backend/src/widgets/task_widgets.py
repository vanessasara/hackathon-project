"""
Task widget utilities for ChatKit.

Provides functions to create structured ListView widgets for displaying tasks.
"""

from typing import Any
from chatkit.widgets import ListView, ListViewItem, Text, Row, Badge, Col


def create_task_list_widget(tasks: list[dict[str, Any]]) -> ListView:
    """
    Create a ListView widget displaying tasks.

    Args:
        tasks: List of task dictionaries with id, title, description, completed fields

    Returns:
        ListView widget with task items

    Example:
        tasks = [
            {"id": 1, "title": "Buy groceries", "description": "Milk, eggs", "completed": False},
            {"id": 2, "title": "Call mom", "description": None, "completed": True}
        ]
        widget = create_task_list_widget(tasks)
    """
    if not tasks:
        return ListView(
            children=[
                ListViewItem(
                    children=[
                        Text(
                            value="No tasks yet! Add one to get started.",
                            color="secondary",
                            italic=True
                        )
                    ]
                )
            ],
            status={"text": "Your Tasks (0)", "icon": {"name": "clipboard-list"}}
        )

    # Separate pending and completed tasks
    pending = [t for t in tasks if not t.get("completed", False)]
    completed = [t for t in tasks if t.get("completed", False)]

    # Build list items
    items = []

    # Pending tasks section
    if pending:
        for task in pending:
            items.append(_create_task_item(task, completed=False))

    # Completed tasks section
    if completed:
        for task in completed:
            items.append(_create_task_item(task, completed=True))

    total_count = len(tasks)
    pending_count = len(pending)

    status_text = f"Your Tasks ({total_count} total"
    if pending_count > 0:
        status_text += f", {pending_count} pending"
    status_text += ")"

    return ListView(
        children=items,
        status={"text": status_text, "icon": {"name": "clipboard-list"}},
        limit="auto"
    )


def _create_task_item(task: dict[str, Any], completed: bool = False) -> ListViewItem:
    """
    Create a single task ListViewItem.

    Args:
        task: Task dictionary with id, title, description, completed
        completed: Whether the task is completed

    Returns:
        ListViewItem for the task
    """
    task_id = task.get("id", "?")
    title = task.get("title", "Untitled task")
    description = task.get("description", "")

    # Create the main content
    children = []

    # Task row with checkbox and title
    task_row_children = []

    # Checkbox emoji (simpler than Icon component)
    checkbox_text = "✅" if completed else "⬜"
    task_row_children.append(
        Text(value=checkbox_text, size="lg")
    )

    # Task title column
    title_col_children = []

    # Title with strikethrough if completed
    title_col_children.append(
        Text(
            value=title,
            weight="semibold",
            lineThrough=completed,
            color="primary" if not completed else "secondary"
        )
    )

    # Description if present
    if description:
        title_col_children.append(
            Text(
                value=description,
                size="sm",
                color="secondary",
                lineThrough=completed
            )
        )

    task_row_children.append(
        Col(children=title_col_children, gap=1)
    )

    # Task ID badge
    task_row_children.append(
        Badge(
            label=f"#{task_id}",
            color="secondary",
            variant="soft",
            size="sm"
        )
    )

    children.append(
        Row(children=task_row_children, gap=3, align="start")
    )

    return ListViewItem(
        children=children,
        gap=2
    )
