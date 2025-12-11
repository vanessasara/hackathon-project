"""
Message model for conversation messages.

A message represents a single message within a conversation.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Message(SQLModel, table=True):
    """Message model for conversation messages."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utc_now, index=True)
