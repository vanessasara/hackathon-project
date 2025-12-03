"""
Task CRUD endpoints for the API.

This module provides RESTful endpoints for managing tasks with user authentication.
All endpoints require a valid JWT token and automatically filter tasks by user_id.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..auth import get_current_user
from ..database import get_session
from ..models.task import Task
from ..models.task_label import TaskLabel
from ..schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TaskFilter(str, Enum):
    """Filter options for task listing."""

    ACTIVE = "active"  # Not deleted, not archived
    TRASH = "trash"  # Soft deleted
    ARCHIVE = "archive"  # Archived
    REMINDERS = "reminders"  # Has reminder_at set


async def _get_task_labels(session: AsyncSession, task_id: int) -> list[int]:
    """Get list of label IDs for a task."""
    statement = select(TaskLabel.label_id).where(TaskLabel.task_id == task_id)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def _task_to_response(session: AsyncSession, task: Task) -> TaskResponse:
    """Convert Task model to TaskResponse with labels."""
    labels = await _get_task_labels(session, task.id)
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        color=task.color,
        pinned=task.pinned,
        archived=task.archived,
        deleted_at=task.deleted_at,
        reminder_at=task.reminder_at,
        created_at=task.created_at,
        updated_at=task.updated_at,
        labels=labels,
    )


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    filter: TaskFilter = Query(TaskFilter.ACTIVE, description="Filter tasks by status"),
    label_id: Optional[int] = Query(None, description="Filter by label ID"),
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[TaskResponse]:
    """
    List tasks for the authenticated user with optional filtering.

    Args:
        filter: Filter by status (active, trash, archive, reminders)
        label_id: Optional label ID to filter by
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        List[TaskResponse]: User's filtered tasks ordered by created_at descending
    """
    # Base query
    statement = select(Task).where(Task.user_id == user_id)

    # Apply filter
    if filter == TaskFilter.ACTIVE:
        statement = statement.where(
            Task.deleted_at.is_(None), Task.archived == False
        )
    elif filter == TaskFilter.TRASH:
        statement = statement.where(Task.deleted_at.is_not(None))
    elif filter == TaskFilter.ARCHIVE:
        statement = statement.where(
            Task.archived == True, Task.deleted_at.is_(None)
        )
    elif filter == TaskFilter.REMINDERS:
        statement = statement.where(
            Task.reminder_at.is_not(None), Task.deleted_at.is_(None)
        )

    # Filter by label if specified
    if label_id is not None:
        statement = statement.join(
            TaskLabel, Task.id == TaskLabel.task_id
        ).where(TaskLabel.label_id == label_id)

    # Order by pinned first, then created_at
    statement = statement.order_by(Task.pinned.desc(), Task.created_at.desc())

    result = await session.execute(statement)
    tasks = result.scalars().all()

    # Convert to response with labels
    responses = []
    for task in tasks:
        responses.append(await _task_to_response(session, task))

    return responses


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        TaskResponse: The newly created task
    """
    # Strip timezone info from reminder_at for naive datetime storage
    reminder_at = task_data.reminder_at
    if reminder_at is not None and hasattr(reminder_at, "tzinfo") and reminder_at.tzinfo is not None:
        reminder_at = reminder_at.replace(tzinfo=None)

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        color=task_data.color,
        pinned=task_data.pinned,
        reminder_at=reminder_at,
        completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return await _task_to_response(session, task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID to retrieve
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        TaskResponse: The requested task

    Raises:
        HTTPException: 404 if task not found, 403 if user doesn't own the task
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return await _task_to_response(session, task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update a task.

    Args:
        task_id: Task ID to update
        task_data: Updated task data
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: 404 if task not found, 403 if user doesn't own the task
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        # Strip timezone info from datetime fields for naive datetime storage
        if field in ("reminder_at", "deleted_at") and value is not None:
            if hasattr(value, "tzinfo") and value.tzinfo is not None:
                value = value.replace(tzinfo=None)
        setattr(task, field, value)

    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return await _task_to_response(session, task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Toggle the completion status of a task.

    Args:
        task_id: ID of the task to toggle
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        TaskResponse: Updated task with toggled completion status

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
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
    return await _task_to_response(session, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Soft delete a task (move to trash).

    Args:
        task_id: ID of the task to delete
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        None: 204 No Content on success

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Soft delete - set deleted_at timestamp
    task.deleted_at = _utc_now()
    task.mark_updated()
    session.add(task)
    await session.commit()


@router.post("/{task_id}/restore", response_model=TaskResponse)
async def restore_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Restore a task from trash.

    Args:
        task_id: ID of the task to restore
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        TaskResponse: The restored task

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Restore - clear deleted_at timestamp
    task.deleted_at = None
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return await _task_to_response(session, task)


@router.delete("/{task_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
async def permanent_delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Permanently delete a task.

    Args:
        task_id: ID of the task to permanently delete
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        None: 204 No Content on success

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Delete task labels first
    statement = select(TaskLabel).where(TaskLabel.task_id == task_id)
    result = await session.execute(statement)
    task_labels = result.scalars().all()
    for tl in task_labels:
        await session.delete(tl)

    # Then delete task
    await session.delete(task)
    await session.commit()


@router.delete("/trash/empty", status_code=status.HTTP_204_NO_CONTENT)
async def empty_trash(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Permanently delete all tasks in trash.

    Args:
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        None: 204 No Content on success
    """
    # Find all trashed tasks for user
    statement = select(Task).where(
        Task.user_id == user_id, Task.deleted_at.is_not(None)
    )
    result = await session.execute(statement)
    trashed_tasks = result.scalars().all()

    # Delete task labels and tasks
    for task in trashed_tasks:
        # Delete labels first
        label_stmt = select(TaskLabel).where(TaskLabel.task_id == task.id)
        label_result = await session.execute(label_stmt)
        for tl in label_result.scalars().all():
            await session.delete(tl)
        # Then delete task
        await session.delete(task)

    await session.commit()


# Label assignment endpoints


@router.post("/{task_id}/labels/{label_id}", status_code=status.HTTP_201_CREATED)
async def add_label_to_task(
    task_id: int,
    label_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Add a label to a task.

    Args:
        task_id: Task ID
        label_id: Label ID to add
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if task/label not found, 403 if not authorized
    """
    from ..models.label import Label

    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    label = await session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if label.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Check if already assigned
    existing = await session.execute(
        select(TaskLabel).where(
            TaskLabel.task_id == task_id, TaskLabel.label_id == label_id
        )
    )
    if existing.scalar_one_or_none():
        return {"message": "Label already assigned"}

    task_label = TaskLabel(task_id=task_id, label_id=label_id)
    session.add(task_label)
    await session.commit()

    return {"message": "Label added"}


@router.delete("/{task_id}/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_label_from_task(
    task_id: int,
    label_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Remove a label from a task.

    Args:
        task_id: Task ID
        label_id: Label ID to remove
        user_id: User ID extracted from JWT token
        session: Database session

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await session.execute(
        select(TaskLabel).where(
            TaskLabel.task_id == task_id, TaskLabel.label_id == label_id
        )
    )
    task_label = result.scalar_one_or_none()
    if task_label:
        await session.delete(task_label)
        await session.commit()
