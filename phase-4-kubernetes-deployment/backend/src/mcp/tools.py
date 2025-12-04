"""
MCP (Model Context Protocol) tools for task management.

These function tools are exposed to AI agents via the Agents SDK.
Tools execute actual database operations using the current context.
"""

import asyncio
import logging
from typing import Optional
from contextvars import ContextVar

from agents import function_tool, RunContextWrapper
from chatkit.agents import AgentContext

logger = logging.getLogger(__name__)

# Context variables to hold current request's session and user_id
_session_context: ContextVar = ContextVar("session_context", default=None)
_user_id_context: ContextVar = ContextVar("user_id_context", default=None)


def set_tool_context(session, user_id):
    """Set the context for tool execution."""
    _session_context.set(session)
    _user_id_context.set(user_id)


def get_tool_context():
    """Get the current tool execution context."""
    return _session_context.get(), _user_id_context.get()


@function_tool
async def add_task(
    title: str,
    description: Optional[str] = None,
) -> dict:
    """
    Add a new task for the user.

    Args:
        title: Task title
        description: Optional task description

    Returns:
        dict: Task creation result

    Example:
        add_task("Buy groceries", "Milk, eggs, bread")
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    logger.info(f"add_task called: title={title}, user_id={user_id}")

    # Import here to avoid circular dependency
    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    # Use async/await directly since the tool is async
    try:
        async with AsyncSession(engine) as session:
            logger.info(f"Creating task in database: {title}")
            task = await task_service.create_task(session, user_id, title, description)
            await session.commit()
            await session.refresh(task)
            logger.info(f"Task created successfully: id={task.id}, title={task.title}")

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
            }
            logger.info(f"Returning success: {result}")
            return result
    except Exception as e:
        logger.error(f"Error executing add_task: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


@function_tool
async def list_tasks(
    ctx: RunContextWrapper[AgentContext],
    status: Optional[str] = None,
) -> None:
    """
    List tasks for the user with optional status filter.

    Args:
        ctx: Agent context for streaming widgets
        status: Optional filter - "all", "pending", or "completed" (default: "all")

    Example:
        list_tasks(status="pending")
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return

    logger.info(f"list_tasks called: status={status}, user_id={user_id}")

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession
    from ..widgets import create_task_list_widget

    try:
        async with AsyncSession(engine) as session:
            tasks = await task_service.list_tasks(session, user_id, status)

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                }
                for task in tasks
            ]

            logger.info(f"Creating widget for {len(tasks)} tasks")

            # Create and stream the widget
            try:
                widget = create_task_list_widget(task_list)
                logger.info(f"Widget created: {type(widget).__name__}")

                await ctx.context.stream_widget(widget)
                logger.info(f"Widget streamed successfully")
            except Exception as widget_error:
                logger.error(f"Error streaming widget: {widget_error}", exc_info=True)
                raise
    except Exception as e:
        logger.error(f"Error executing list_tasks: {e}", exc_info=True)


@function_tool
async def complete_task(
    task_id: int,
) -> dict:
    """
    Mark a task as complete (or toggle if already complete).

    Args:
        task_id: Task ID to complete

    Returns:
        dict: Updated task details

    Example:
        complete_task(42)
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    logger.info(f"complete_task called: task_id={task_id}, user_id={user_id}")

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    try:
        async with AsyncSession(engine) as session:
            task = await task_service.toggle_complete(session, user_id, task_id)

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
            }
            logger.info(f"Task {task_id} toggled to completed={task.completed}")
            return result
    except Exception as e:
        logger.error(f"Error executing complete_task: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


@function_tool
async def delete_task(
    task_id: int,
) -> dict:
    """
    Delete a task (moves to trash, soft delete).

    Args:
        task_id: Task ID to delete

    Returns:
        dict: Deleted task details

    Example:
        delete_task(42)
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    logger.info(f"delete_task called: task_id={task_id}, user_id={user_id}")

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    try:
        async with AsyncSession(engine) as session:
            task = await task_service.delete_task(session, user_id, task_id)

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
            }
            logger.info(f"Task {task_id} deleted successfully")
            return result
    except Exception as e:
        logger.error(f"Error executing delete_task: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


@function_tool
async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """
    Update a task's title and/or description.

    Args:
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        dict: Updated task details

    Example:
        update_task(42, title="Call mom tonight")
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    logger.info(f"update_task called: task_id={task_id}, user_id={user_id}")

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    try:
        async with AsyncSession(engine) as session:
            task = await task_service.update_task(
                session, user_id, task_id,
                title=title,
                description=description
            )

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
            }
            logger.info(f"Task {task_id} updated successfully")
            return result
    except Exception as e:
        logger.error(f"Error executing update_task: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }
