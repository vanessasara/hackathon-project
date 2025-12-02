"""
Task SQLModel for database operations.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task model representing a todo item in the database.

    Attributes:
        id: Primary key, auto-generated
        user_id: Reference to the user who owns this task (from Better Auth)
        title: Task title (max 200 characters)
        description: Optional detailed description (max 1000 characters)
        completed: Boolean flag for completion status
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
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    def mark_updated(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.utcnow()
