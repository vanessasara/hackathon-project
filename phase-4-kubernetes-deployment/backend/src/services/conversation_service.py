"""
Conversation service layer for managing chat conversations and messages.

Provides CRUD operations for conversations and messages.
"""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.conversation import Conversation
from ..models.message import Message


async def create_conversation(
    session: AsyncSession,
    user_id: str,
) -> Conversation:
    """
    Create a new conversation for a user.

    Args:
        session: Database session
        user_id: Owner user ID

    Returns:
        Conversation: The created conversation

    Example:
        conv = await create_conversation(session, "user123")
    """
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation(
    session: AsyncSession,
    user_id: str,
    conversation_id: int,
) -> Conversation:
    """
    Get a conversation by ID (with ownership check).

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        conversation_id: Conversation ID

    Returns:
        Conversation: The requested conversation

    Raises:
        HTTPException: 404 if not found or not authorized

    Example:
        conv = await get_conversation(session, "user123", 42)
    """
    conversation = await session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


async def list_conversations(
    session: AsyncSession,
    user_id: str,
    limit: int = 20,
) -> list[Conversation]:
    """
    List user's conversations ordered by most recent.

    Args:
        session: Database session
        user_id: Owner user ID
        limit: Maximum number of conversations to return

    Returns:
        list[Conversation]: User's conversations

    Example:
        convs = await list_conversations(session, "user123", limit=10)
    """
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def add_message(
    session: AsyncSession,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_calls: Optional[dict] = None,
) -> Message:
    """
    Add a message to a conversation.

    Args:
        session: Database session
        conversation_id: Conversation ID
        user_id: User ID (for denormalization)
        role: Message role ("user" or "assistant")
        content: Message content
        tool_calls: Optional tool calls metadata (for assistant messages)

    Returns:
        Message: The created message

    Example:
        msg = await add_message(
            session, 42, "user123", "user", "Add a task to buy groceries"
        )
    """
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
    )
    session.add(message)

    # Update conversation timestamp
    conversation = await session.get(Conversation, conversation_id)
    if conversation:
        conversation.mark_updated()
        session.add(conversation)

    await session.commit()
    await session.refresh(message)
    return message


async def get_conversation_messages(
    session: AsyncSession,
    conversation_id: int,
) -> list[Message]:
    """
    Get all messages in a conversation ordered by time.

    Args:
        session: Database session
        conversation_id: Conversation ID

    Returns:
        list[Message]: Messages ordered by created_at

    Example:
        messages = await get_conversation_messages(session, 42)
    """
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def delete_conversation(
    session: AsyncSession,
    user_id: str,
    conversation_id: int,
) -> None:
    """
    Delete a conversation and all its messages.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        conversation_id: Conversation ID to delete

    Raises:
        HTTPException: 404 if not found or not authorized

    Example:
        await delete_conversation(session, "user123", 42)
    """
    conversation = await get_conversation(session, user_id, conversation_id)

    # Delete all messages first
    messages_stmt = select(Message).where(Message.conversation_id == conversation_id)
    messages_result = await session.execute(messages_stmt)
    for message in messages_result.scalars().all():
        await session.delete(message)

    # Then delete conversation
    await session.delete(conversation)
    await session.commit()
