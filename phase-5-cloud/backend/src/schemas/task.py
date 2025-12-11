"""
Pydantic schemas for Task API request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Attributes:
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
        color: Note background color key (default: "default")
        pinned: Whether note is pinned to top
        reminder_at: Optional reminder timestamp
        due_at: Optional due date/deadline (Part B)
        is_recurring: Whether this is a recurring task (Part B)
        recurrence_rule: Recurrence pattern (Part B)
        recurrence_end: End date for recurring series (Part B)
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description"
    )
    color: str = Field(default="default", max_length=20, description="Note color key")
    pinned: bool = Field(default=False, description="Whether note is pinned")
    reminder_at: Optional[datetime] = Field(
        default=None, description="When to remind user about this task"
    )
    # Part B: Advanced Features
    due_at: Optional[datetime] = Field(
        default=None, description="Task due date/time (deadline)"
    )
    is_recurring: bool = Field(
        default=False, description="Whether this is a recurring task"
    )
    recurrence_rule: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Recurrence pattern: daily, weekly, monthly, weekdays, or cron:expression",
    )
    recurrence_end: Optional[datetime] = Field(
        default=None, description="When recurring task should stop creating new occurrences"
    )


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated task title
        description: Updated task description
        completed: Updated completion status
        color: Note background color key
        pinned: Whether note is pinned
        archived: Whether note is archived
        reminder_at: When to remind user (None to clear)
        due_at: Task deadline (Part B)
        is_recurring: Whether task is recurring (Part B)
        recurrence_rule: Recurrence pattern (Part B)
        recurrence_end: End date for recurring series (Part B)
    """

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=200, description="Task title"
    )
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description"
    )
    completed: Optional[bool] = Field(default=None, description="Completion status")
    color: Optional[str] = Field(default=None, max_length=20, description="Note color key")
    pinned: Optional[bool] = Field(default=None, description="Whether note is pinned")
    archived: Optional[bool] = Field(default=None, description="Whether note is archived")
    reminder_at: Optional[datetime] = Field(
        default=None, description="When to remind user about this task"
    )
    # Part B: Advanced Features
    due_at: Optional[datetime] = Field(
        default=None, description="Task due date/time (deadline)"
    )
    is_recurring: Optional[bool] = Field(
        default=None, description="Whether this is a recurring task"
    )
    recurrence_rule: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Recurrence pattern: daily, weekly, monthly, weekdays, or cron:expression",
    )
    recurrence_end: Optional[datetime] = Field(
        default=None, description="When recurring task should stop creating new occurrences"
    )


class TaskResponse(BaseModel):
    """
    Schema for task responses.

    This is the complete representation of a task returned by the API.

    Attributes:
        id: Task ID
        user_id: Owner's user ID
        title: Task title
        description: Task description (may be None)
        completed: Completion status
        color: Note background color key
        pinned: Whether note is pinned
        archived: Whether note is archived
        deleted_at: Soft delete timestamp (None = active)
        reminder_at: When to remind user
        reminder_sent: Whether reminder was sent (Part B)
        due_at: Task deadline (Part B)
        is_recurring: Whether task is recurring (Part B)
        recurrence_rule: Recurrence pattern (Part B)
        recurrence_end: End date for recurring series (Part B)
        parent_task_id: Link to original recurring task (Part B)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        labels: List of label IDs assigned to this task
    """

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    color: str
    pinned: bool
    archived: bool
    deleted_at: Optional[datetime]
    reminder_at: Optional[datetime]
    # Part B: Advanced Features
    reminder_sent: bool = False
    due_at: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    recurrence_end: Optional[datetime] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    labels: list[int] = []  # List of label IDs

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel compatibility
