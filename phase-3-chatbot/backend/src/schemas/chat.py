"""
Pydantic schemas for chat API requests and responses.

Defines the structure for chat messages, requests, and streaming events.
"""

from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for sending a chat message."""

    conversation_id: Optional[int] = Field(
        None, description="ID of existing conversation (omit to start new)"
    )
    message: str = Field(
        ..., description="User's natural language message", min_length=1, max_length=4000
    )


class ChatResponse(BaseModel):
    """Response body for chat completion (non-streaming)."""

    conversation_id: int = Field(..., description="ID of the conversation")
    message: str = Field(..., description="Assistant's response")
    tool_calls: Optional[list[dict]] = Field(
        None, description="MCP tools that were invoked"
    )
