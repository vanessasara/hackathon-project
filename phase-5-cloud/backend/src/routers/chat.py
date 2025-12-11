"""
Chat endpoint for AI-powered natural language task management.

Handles incoming chat requests and streams responses from the todo agent.
Uses stateless architecture with conversation state persisted to database.
"""

import json
import logging
from typing import AsyncIterator

from agents import RawResponsesStreamEvent, Runner
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from ..agents.todo_agent import create_todo_agent
from ..auth import get_current_user
from ..database import get_session
from ..schemas.chat import ChatRequest
from ..services import conversation_service, task_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Singleton todo agent instance
_todo_agent = None


def get_todo_agent():
    """Get or create the todo agent singleton."""
    global _todo_agent
    if _todo_agent is None:
        _todo_agent = create_todo_agent()
    return _todo_agent


async def execute_tool_call(
    tool_name: str,
    tool_args: dict,
    user_id: str,
    session: AsyncSession,
) -> dict:
    """
    Execute MCP tool calls and perform actual database operations.

    Args:
        tool_name: Name of the tool being called
        tool_args: Arguments passed to the tool
        user_id: Current user ID
        session: Database session

    Returns:
        dict: Result of the tool execution
    """
    try:
        if tool_name == "add_task":
            task = await task_service.create_task(
                session=session,
                user_id=user_id,
                title=tool_args.get("title"),
                description=tool_args.get("description"),
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' created successfully"
            }

        elif tool_name == "list_tasks":
            status_filter = tool_args.get("status", "all")
            tasks = await task_service.list_tasks(
                session=session,
                user_id=user_id,
                status_filter=status_filter,
            )
            return {
                "success": True,
                "count": len(tasks),
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                    }
                    for t in tasks
                ]
            }

        elif tool_name == "complete_task":
            task_id = tool_args.get("task_id")
            task = await task_service.toggle_complete(
                session=session,
                user_id=user_id,
                task_id=task_id,
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
                "message": f"Task '{task.title}' marked as {'complete' if task.completed else 'incomplete'}"
            }

        elif tool_name == "delete_task":
            task_id = tool_args.get("task_id")
            await task_service.delete_task(
                session=session,
                user_id=user_id,
                task_id=task_id,
            )
            return {
                "success": True,
                "task_id": task_id,
                "message": f"Task {task_id} deleted successfully"
            }

        elif tool_name == "update_task":
            task_id = tool_args.get("task_id")
            title = tool_args.get("title")
            description = tool_args.get("description")

            task = await task_service.update_task(
                session=session,
                user_id=user_id,
                task_id=task_id,
                title=title,
                description=description,
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' updated successfully"
            }

        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def handle_chat_stream(
    request: ChatRequest,
    user_id: str,
    session: AsyncSession,
) -> AsyncIterator[dict]:
    """
    Handle a chat request and stream the agent's response.

    Args:
        request: The validated chat request
        user_id: Authenticated user ID
        session: Database session

    Yields:
        dict: Server-Sent Event payloads

    The function:
    1. Creates/loads conversation
    2. Builds message history from database
    3. Runs the todo agent with streaming enabled
    4. Converts agent output chunks to SSE format
    5. Saves messages to database
    6. Handles errors gracefully
    """
    try:
        # Get the todo agent
        agent = get_todo_agent()

        # Get or create conversation
        if request.conversation_id:
            try:
                conversation = await conversation_service.get_conversation(
                    session, user_id, request.conversation_id
                )
            except HTTPException:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = await conversation_service.create_conversation(session, user_id)

        logger.info(
            f"Processing chat for user {user_id}, conversation {conversation.id}: {request.message[:100]}"
        )

        # Build conversation history from database
        messages = await conversation_service.get_conversation_messages(
            session, conversation.id
        )

        # Format: list of {"role": "user"|"assistant", "content": "..."}
        conversation_input = []
        for msg in messages:
            if msg.role in ("user", "assistant"):
                conversation_input.append({"role": msg.role, "content": msg.content})

        # Add current user message
        conversation_input.append({"role": "user", "content": request.message})

        # Save user message to database
        await conversation_service.add_message(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message,
        )

        # Set tool context for MCP tool execution
        from ..mcp.tools import set_tool_context
        set_tool_context(session, user_id)

        # Run the agent with streaming
        result = Runner.run_streamed(starting_agent=agent, input=conversation_input)

        # Stream the response chunks
        accumulated_response = ""
        tool_calls_log = []

        async for event in result.stream_events():
            # Handle raw response events which contain the streaming text
            if isinstance(event, RawResponsesStreamEvent):
                data = event.data
                # Check for text delta events
                if hasattr(data, "type") and data.type == "response.output_text.delta":
                    if hasattr(data, "delta") and data.delta:
                        text = data.delta
                        accumulated_response += text

                        # Yield text delta event
                        yield {
                            "type": "text_delta",
                            "content": text,
                        }

        # Log the final response
        logger.info(
            f"Completed chat for conversation {conversation.id}: {len(accumulated_response)} chars"
        )

        # Save assistant message to database
        await conversation_service.add_message(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=accumulated_response,
            tool_calls={"calls": tool_calls_log} if tool_calls_log else None,
        )

        # Yield completion event
        yield {
            "type": "done",
            "conversation_id": conversation.id,
            "tool_calls": tool_calls_log,
        }

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing chat request: {e}", exc_info=True)

        # Yield user-friendly error event
        yield {
            "type": "error",
            "error": "Sorry, I encountered an error processing your request. Please try again.",
        }


@router.post("")
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Send a chat message to the AI todo assistant.

    Returns Server-Sent Events (SSE) with streaming response.

    Args:
        request: Chat request with message and optional conversation_id
        user_id: Authenticated user ID from JWT
        session: Database session

    Returns:
        EventSourceResponse: SSE stream with text deltas and completion

    Event Types:
        - text_delta: {"type": "text_delta", "content": "partial text"}
        - done: {"type": "done", "conversation_id": 123, "tool_calls": [...]}
        - error: {"type": "error", "error": "error message"}

    Example:
        POST /api/chat
        {
            "message": "Add a task to buy groceries"
        }

        Response (SSE):
        data: {"type": "text_delta", "content": "I've added"}
        data: {"type": "text_delta", "content": " a task"}
        data: {"type": "done", "conversation_id": 42, "tool_calls": []}
    """

    async def event_generator():
        async for data in handle_chat_stream(request, user_id, session):
            yield {"data": json.dumps(data)}

    return EventSourceResponse(event_generator())


@router.get("/conversations")
async def list_conversations(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    List user's conversations ordered by most recent.

    Args:
        user_id: Authenticated user ID from JWT
        session: Database session

    Returns:
        list: User's conversations with metadata
    """
    conversations = await conversation_service.list_conversations(session, user_id, limit=20)

    return [
        {
            "id": conv.id,
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
        }
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Get a conversation with all its messages.

    Args:
        conversation_id: Conversation ID
        user_id: Authenticated user ID from JWT
        session: Database session

    Returns:
        dict: Conversation with messages

    Raises:
        HTTPException: 404 if conversation not found or not authorized
    """
    conversation = await conversation_service.get_conversation(
        session, user_id, conversation_id
    )
    messages = await conversation_service.get_conversation_messages(session, conversation_id)

    return {
        "id": conversation.id,
        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "tool_calls": msg.tool_calls,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            }
            for msg in messages
        ],
    }


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: Conversation ID
        user_id: Authenticated user ID from JWT
        session: Database session

    Returns:
        None: 204 No Content on success

    Raises:
        HTTPException: 404 if conversation not found or not authorized
    """
    await conversation_service.delete_conversation(session, user_id, conversation_id)
