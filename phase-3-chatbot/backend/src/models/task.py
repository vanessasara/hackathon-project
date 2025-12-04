"""
Task SQLModel for database operations.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime (without timezone info)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Task(SQLModel, table=True):
    """
    Task model representing a todo item in the database.

    Attributes:
        id: Primary key, auto-generated
        user_id: Reference to the user who owns this task (from Better Auth)
        title: Task title (max 200 characters)
        description: Optional detailed description (max 1000 characters)
        completed: Boolean flag for completion status
        color: Note background color key
        pinned: Whether note is pinned to top
        archived: Whether note is archived
        deleted_at: Soft delete timestamp (None = active)
        reminder_at: When to remind user about this task
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="User ID from Better Auth")
    title: str = Field(max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description"
    )
    completed: bool = Field(default=False, description="Completion status")
    color: str = Field(default="default", max_length=20, description="Note color key")
    pinned: bool = Field(default=False, description="Whether note is pinned")
    archived: bool = Field(default=False, index=True, description="Whether note is archived")
    deleted_at: Optional[datetime] = Field(
        default=None, index=True, description="Soft delete timestamp (None = active)"
    )
    reminder_at: Optional[datetime] = Field(
        default=None, index=True, description="When to remind user about this task"
    )
    created_at: datetime = Field(
        default_factory=_utc_now,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=_utc_now,
        description="Last update timestamp",
    )

    def mark_updated(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = _utc_now()
