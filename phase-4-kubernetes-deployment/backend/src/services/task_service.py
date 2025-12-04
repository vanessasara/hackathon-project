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
) -> Task:
    """
    Create a new task.

    Args:
        session: Database session
        user_id: Owner user ID
        title: Task title
        description: Optional task description

    Returns:
        Task: The created task

    Example:
        task = await create_task(session, "user123", "Buy groceries")
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
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
