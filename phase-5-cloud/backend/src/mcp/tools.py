"""
MCP (Model Context Protocol) tools for task management.

These function tools are exposed to AI agents via the Agents SDK.
Tools execute actual database operations using the current context.

Part B: Advanced Features adds tools for:
- Setting reminders: "remind me about X at Y"
- Creating recurring tasks: "add daily task X"
- Rescheduling tasks: "reschedule X to Y"
- Listing tasks with reminders
- Listing recurring tasks
"""

import asyncio
import logging
from datetime import datetime, timedelta
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


# =============================================================================
# Part B: Advanced Features - Reminder and Recurring Task Tools
# =============================================================================


def _parse_datetime(datetime_str: str) -> Optional[datetime]:
    """
    Parse a datetime string into a datetime object.
    Supports various formats like:
    - ISO format: "2024-12-25T09:00:00"
    - Date and time: "2024-12-25 09:00"
    - Relative: "tomorrow", "in 2 hours", "next monday"
    """
    from datetime import timezone
    import re

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Handle relative dates
    datetime_lower = datetime_str.lower().strip()

    if datetime_lower == "tomorrow":
        return now + timedelta(days=1)
    elif datetime_lower == "today":
        return now
    elif datetime_lower.startswith("in "):
        # Parse "in X hours/minutes/days"
        match = re.match(r"in (\d+) (hour|minute|day|week)s?", datetime_lower)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if unit == "minute":
                return now + timedelta(minutes=amount)
            elif unit == "hour":
                return now + timedelta(hours=amount)
            elif unit == "day":
                return now + timedelta(days=amount)
            elif unit == "week":
                return now + timedelta(weeks=amount)
    elif "monday" in datetime_lower or "tuesday" in datetime_lower or "wednesday" in datetime_lower or \
         "thursday" in datetime_lower or "friday" in datetime_lower or "saturday" in datetime_lower or \
         "sunday" in datetime_lower:
        # Handle "next monday", "this friday", etc.
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, day in enumerate(days):
            if day in datetime_lower:
                current_day = now.weekday()
                target_day = i
                days_ahead = target_day - current_day
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                return now + timedelta(days=days_ahead)

    # Try parsing ISO format and other common formats
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue

    return None


@function_tool
async def set_reminder(
    task_id: int,
    reminder_time: str,
) -> dict:
    """
    Set a reminder for a task. The user will receive a notification at the specified time.

    Args:
        task_id: Task ID to set reminder for
        reminder_time: When to remind - can be ISO datetime (2024-12-25T09:00),
                      relative (tomorrow, in 2 hours, next monday), or date string

    Returns:
        dict: Updated task with reminder info

    Example:
        set_reminder(42, "tomorrow")
        set_reminder(42, "in 2 hours")
        set_reminder(42, "2024-12-25 09:00")
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    logger.info(f"set_reminder called: task_id={task_id}, reminder_time={reminder_time}, user_id={user_id}")

    reminder_dt = _parse_datetime(reminder_time)
    if not reminder_dt:
        return {"success": False, "error": f"Could not parse datetime: {reminder_time}"}

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    try:
        async with AsyncSession(engine) as session:
            task = await task_service.set_reminder(session, user_id, task_id, reminder_dt)

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "reminder_at": task.reminder_at.isoformat() if task.reminder_at else None,
            }
            logger.info(f"Reminder set for task {task_id} at {reminder_dt}")
            return result
    except Exception as e:
        logger.error(f"Error executing set_reminder: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@function_tool
async def reschedule_task(
    task_id: int,
    new_time: str,
) -> dict:
    """
    Reschedule a task's reminder to a new date/time.

    Args:
        task_id: Task ID to reschedule
        new_time: New reminder time - can be ISO datetime, relative, or date string

    Returns:
        dict: Updated task with new reminder time

    Example:
        reschedule_task(42, "next monday")
        reschedule_task(42, "in 1 week")
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    logger.info(f"reschedule_task called: task_id={task_id}, new_time={new_time}, user_id={user_id}")

    new_dt = _parse_datetime(new_time)
    if not new_dt:
        return {"success": False, "error": f"Could not parse datetime: {new_time}"}

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    try:
        async with AsyncSession(engine) as session:
            task = await task_service.reschedule_task(session, user_id, task_id, new_dt)

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "reminder_at": task.reminder_at.isoformat() if task.reminder_at else None,
            }
            logger.info(f"Task {task_id} rescheduled to {new_dt}")
            return result
    except Exception as e:
        logger.error(f"Error executing reschedule_task: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@function_tool
async def add_recurring_task(
    title: str,
    recurrence_pattern: str,
    description: Optional[str] = None,
    end_date: Optional[str] = None,
) -> dict:
    """
    Create a recurring task that automatically creates new instances when completed.

    Args:
        title: Task title
        recurrence_pattern: How often to repeat - "daily", "weekly", "monthly", "weekdays"
        description: Optional task description
        end_date: Optional end date for recurrence (ISO datetime or relative)

    Returns:
        dict: Created recurring task details

    Example:
        add_recurring_task("Team standup", "weekdays")
        add_recurring_task("Weekly review", "weekly", end_date="2025-03-01")
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return {"error": "No active user context"}

    valid_patterns = ["daily", "weekly", "monthly", "weekdays"]
    if recurrence_pattern.lower() not in valid_patterns:
        return {
            "success": False,
            "error": f"Invalid recurrence pattern. Must be one of: {', '.join(valid_patterns)}"
        }

    logger.info(f"add_recurring_task called: title={title}, pattern={recurrence_pattern}, user_id={user_id}")

    recurrence_end_dt = None
    if end_date:
        recurrence_end_dt = _parse_datetime(end_date)

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession

    try:
        async with AsyncSession(engine) as session:
            task = await task_service.create_task(
                session, user_id, title, description,
                is_recurring=True,
                recurrence_rule=recurrence_pattern.lower(),
                recurrence_end=recurrence_end_dt,
            )

            result = {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "is_recurring": task.is_recurring,
                "recurrence_rule": task.recurrence_rule,
                "recurrence_end": task.recurrence_end.isoformat() if task.recurrence_end else None,
            }
            logger.info(f"Recurring task created: id={task.id}, pattern={recurrence_pattern}")
            return result
    except Exception as e:
        logger.error(f"Error executing add_recurring_task: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@function_tool
async def list_tasks_with_reminders(
    ctx: RunContextWrapper[AgentContext],
) -> None:
    """
    List all tasks that have reminders set, ordered by reminder time.

    Args:
        ctx: Agent context for streaming widgets

    Example:
        list_tasks_with_reminders()
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return

    logger.info(f"list_tasks_with_reminders called: user_id={user_id}")

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession
    from ..widgets import create_task_list_widget

    try:
        async with AsyncSession(engine) as session:
            tasks = await task_service.list_tasks_with_reminders(session, user_id)

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "reminder_at": task.reminder_at.isoformat() if task.reminder_at else None,
                }
                for task in tasks
            ]

            logger.info(f"Found {len(tasks)} tasks with reminders")

            widget = create_task_list_widget(task_list)
            await ctx.context.stream_widget(widget)
            logger.info(f"Widget streamed successfully")
    except Exception as e:
        logger.error(f"Error executing list_tasks_with_reminders: {e}", exc_info=True)


@function_tool
async def list_recurring_tasks(
    ctx: RunContextWrapper[AgentContext],
) -> None:
    """
    List all recurring tasks.

    Args:
        ctx: Agent context for streaming widgets

    Example:
        list_recurring_tasks()
    """
    _, user_id = get_tool_context()
    if not user_id:
        logger.error("No user_id in context")
        return

    logger.info(f"list_recurring_tasks called: user_id={user_id}")

    from ..services import task_service
    from ..database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession
    from ..widgets import create_task_list_widget

    try:
        async with AsyncSession(engine) as session:
            tasks = await task_service.list_recurring_tasks(session, user_id)

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "is_recurring": task.is_recurring,
                    "recurrence_rule": task.recurrence_rule,
                }
                for task in tasks
            ]

            logger.info(f"Found {len(tasks)} recurring tasks")

            widget = create_task_list_widget(task_list)
            await ctx.context.stream_widget(widget)
            logger.info(f"Widget streamed successfully")
    except Exception as e:
        logger.error(f"Error executing list_recurring_tasks: {e}", exc_info=True)
