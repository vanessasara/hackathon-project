"""
Task service layer for business logic.

Provides reusable functions for task CRUD operations that can be used by
both REST endpoints and MCP tools.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def create_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    reminder_at: Optional[datetime] = None,
    is_recurring: bool = False,
    recurrence_rule: Optional[str] = None,
    recurrence_end: Optional[datetime] = None,
) -> Task:
    """
    Create a new task.

    Args:
        session: Database session
        user_id: Owner user ID
        title: Task title
        description: Optional task description
        reminder_at: Optional reminder datetime (Part B)
        is_recurring: Whether this is a recurring task (Part B)
        recurrence_rule: Recurrence pattern - daily, weekly, monthly, weekdays (Part B)
        recurrence_end: Optional end date for recurrence (Part B)

    Returns:
        Task: The created task

    Example:
        task = await create_task(session, "user123", "Buy groceries")
        task = await create_task(session, "user123", "Standup", is_recurring=True, recurrence_rule="weekdays")
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
        reminder_at=reminder_at,
        is_recurring=is_recurring,
        recurrence_rule=recurrence_rule,
        recurrence_end=recurrence_end,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status: Optional[str] = None,
) -> list[Task]:
    """
    List tasks for a user with optional status filter.

    Args:
        session: Database session
        user_id: Owner user ID
        status: Optional filter - "all", "pending", or "completed" (default: "all")

    Returns:
        list[Task]: Filtered list of tasks ordered by created_at desc

    Example:
        tasks = await list_tasks(session, "user123", status="pending")
    """
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.deleted_at.is_(None)  # Exclude soft-deleted tasks
    )

    # Apply status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    # If status is "all" or None, return all tasks

    # Order by pinned first, then created_at desc
    statement = statement.order_by(Task.pinned.desc(), Task.created_at.desc())

    result = await session.execute(statement)
    return list(result.scalars().all())


async def toggle_complete(
    session: AsyncSession,
    user_id: str,
    task_id: int,
) -> Task:
    """
    Toggle the completion status of a task.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to toggle

    Returns:
        Task: Updated task

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized

    Example:
        task = await toggle_complete(session, "user123", 42)
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.completed = not task.completed
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
) -> Task:
    """
    Soft delete a task (move to trash).

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to delete

    Returns:
        Task: Deleted task

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized

    Example:
        task = await delete_task(session, "user123", 42)
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.deleted_at = _utc_now()
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Task:
    """
    Update a task's title and/or description.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        Task: Updated task

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized

    Example:
        task = await update_task(
            session, "user123", 42,
            title="Call mom tonight"
        )
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


# =============================================================================
# Part B: Advanced Features - Reminder and Recurring Task Services
# =============================================================================


async def set_reminder(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    reminder_at: datetime,
) -> Task:
    """
    Set a reminder for a task.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to set reminder for
        reminder_at: When to send the reminder

    Returns:
        Task: Updated task with reminder

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized

    Example:
        task = await set_reminder(session, "user123", 42, datetime(2024, 12, 25, 9, 0))
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.reminder_at = reminder_at
    task.reminder_sent = False  # Reset sent flag when setting new reminder
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def remove_reminder(
    session: AsyncSession,
    user_id: str,
    task_id: int,
) -> Task:
    """
    Remove a reminder from a task.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to remove reminder from

    Returns:
        Task: Updated task without reminder

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.reminder_at = None
    task.reminder_sent = False
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def reschedule_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    new_datetime: datetime,
) -> Task:
    """
    Reschedule a task's reminder to a new datetime.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to reschedule
        new_datetime: New reminder datetime

    Returns:
        Task: Updated task with rescheduled reminder

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized

    Example:
        task = await reschedule_task(session, "user123", 42, datetime(2024, 12, 26, 10, 0))
    """
    return await set_reminder(session, user_id, task_id, new_datetime)


async def list_tasks_with_reminders(
    session: AsyncSession,
    user_id: str,
) -> list[Task]:
    """
    List all tasks that have reminders set.

    Args:
        session: Database session
        user_id: Owner user ID

    Returns:
        list[Task]: Tasks with reminders, ordered by reminder_at ascending

    Example:
        tasks = await list_tasks_with_reminders(session, "user123")
    """
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.deleted_at.is_(None),
        Task.reminder_at.is_not(None),
    ).order_by(Task.reminder_at.asc())

    result = await session.execute(statement)
    return list(result.scalars().all())


async def list_recurring_tasks(
    session: AsyncSession,
    user_id: str,
) -> list[Task]:
    """
    List all recurring tasks.

    Args:
        session: Database session
        user_id: Owner user ID

    Returns:
        list[Task]: Recurring tasks ordered by created_at desc

    Example:
        tasks = await list_recurring_tasks(session, "user123")
    """
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.deleted_at.is_(None),
        Task.is_recurring == True,
    ).order_by(Task.created_at.desc())

    result = await session.execute(statement)
    return list(result.scalars().all())


async def set_recurring(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    recurrence_rule: str,
    recurrence_end: Optional[datetime] = None,
) -> Task:
    """
    Make a task recurring with a specified pattern.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to make recurring
        recurrence_rule: Pattern - "daily", "weekly", "monthly", "weekdays"
        recurrence_end: Optional end date for the recurrence

    Returns:
        Task: Updated task with recurring settings

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized

    Example:
        task = await set_recurring(session, "user123", 42, "daily")
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.is_recurring = True
    task.recurrence_rule = recurrence_rule
    task.recurrence_end = recurrence_end
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def remove_recurring(
    session: AsyncSession,
    user_id: str,
    task_id: int,
) -> Task:
    """
    Remove recurring settings from a task.

    Args:
        session: Database session
        user_id: Owner user ID (for authorization)
        task_id: Task ID to remove recurring from

    Returns:
        Task: Updated task without recurring settings

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.is_recurring = False
    task.recurrence_rule = None
    task.recurrence_end = None
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
