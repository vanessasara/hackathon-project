"""
Label SQLModel for organizing tasks with labels.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime (without timezone info)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Label(SQLModel, table=True):
    """
    Label model for organizing tasks.

    Attributes:
        id: Primary key, auto-generated
        user_id: Reference to the user who owns this label
        name: Label name (max 50 characters)
        created_at: Timestamp when label was created
        updated_at: Timestamp when label was last updated
    """

    __tablename__ = "labels"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="User ID from Better Auth")
    name: str = Field(max_length=50, description="Label name")
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
