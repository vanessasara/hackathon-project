"""
Pydantic schemas for Label API request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LabelCreate(BaseModel):
    """
    Schema for creating a new label.

    Attributes:
        name: Label name (required, 1-50 characters)
    """

    name: str = Field(..., min_length=1, max_length=50, description="Label name")


class LabelUpdate(BaseModel):
    """
    Schema for updating an existing label.

    Attributes:
        name: Updated label name
    """

    name: Optional[str] = Field(
        default=None, min_length=1, max_length=50, description="Label name"
    )


class LabelResponse(BaseModel):
    """
    Schema for label responses.

    Attributes:
        id: Label ID
        user_id: Owner's user ID
        name: Label name
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel compatibility
