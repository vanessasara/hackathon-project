"""
Conversation model for chat sessions.

A conversation represents a chat session belonging to a user.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=_utc_now, index=True)
    updated_at: datetime = Field(default_factory=_utc_now, index=True)

    def mark_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = _utc_now()
