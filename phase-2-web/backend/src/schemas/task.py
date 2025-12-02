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
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description"
    )


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated task title
        description: Updated task description
        completed: Updated completion status
    """

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=200, description="Task title"
    )
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description"
    )
    completed: Optional[bool] = Field(default=None, description="Completion status")


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
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel compatibility
