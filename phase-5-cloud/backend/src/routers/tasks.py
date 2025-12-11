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
        # Part B: Advanced Features
        reminder_sent=task.reminder_sent,
        due_at=task.due_at,
        is_recurring=task.is_recurring,
        recurrence_rule=task.recurrence_rule,
        recurrence_end=task.recurrence_end,
        parent_task_id=task.parent_task_id,
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


def _strip_tz(dt: Optional[datetime]) -> Optional[datetime]:
    """Strip timezone info from datetime for naive datetime storage."""
    if dt is not None and hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


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
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        color=task_data.color,
        pinned=task_data.pinned,
        reminder_at=_strip_tz(task_data.reminder_at),
        # Part B: Advanced Features
        due_at=_strip_tz(task_data.due_at),
        is_recurring=task_data.is_recurring,
        recurrence_rule=task_data.recurrence_rule,
        recurrence_end=_strip_tz(task_data.recurrence_end),
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
    datetime_fields = ("reminder_at", "deleted_at", "due_at", "recurrence_end")
    for field, value in update_data.items():
        # Strip timezone info from datetime fields for naive datetime storage
        if field in datetime_fields and value is not None:
            value = _strip_tz(value)
        setattr(task, field, value)

    # Reset reminder_sent if reminder_at is updated (Part B)
    if "reminder_at" in update_data:
        task.reminder_sent = False

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

    For recurring tasks, completing the task will:
    1. Mark the current occurrence as completed
    2. Create a new task for the next occurrence (if within recurrence_end)
    3. Publish a task-completed event for event-driven workflows

    Args:
        task_id: ID of the task to toggle
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        TaskResponse: Updated task with toggled completion status

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    from ..dapr_client import publish_task_event
    from ..utils.recurrence import calculate_next_occurrence

    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Toggle completion
    task.completed = not task.completed
    task.mark_updated()

    # Part B: Handle recurring task completion
    next_task = None
    if task.completed and task.is_recurring and task.recurrence_rule:
        # Calculate the base date for next occurrence
        base_date = task.reminder_at or task.due_at or _utc_now()

        # Calculate next occurrence
        next_date = calculate_next_occurrence(
            current_date=base_date,
            recurrence_rule=task.recurrence_rule,
            recurrence_end=task.recurrence_end,
        )

        if next_date:
            # Create next occurrence as a new task
            next_task = Task(
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                color=task.color,
                pinned=task.pinned,
                archived=False,
                completed=False,
                # Set the next reminder/due date
                reminder_at=next_date if task.reminder_at else None,
                due_at=next_date if task.due_at and not task.reminder_at else None,
                reminder_sent=False,
                # Carry over recurring settings
                is_recurring=True,
                recurrence_rule=task.recurrence_rule,
                recurrence_end=task.recurrence_end,
                # Link to original task
                parent_task_id=task.parent_task_id or task.id,
            )
            session.add(next_task)

            # Mark original task as no longer recurring (it's now a completed occurrence)
            task.is_recurring = False

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Publish task-completed event for event-driven workflows
    if task.completed:
        task_data = {
            "title": task.title,
            "completed": task.completed,
            "next_occurrence_id": next_task.id if next_task else None,
        }
        await publish_task_event(
            event_type="completed",
            task_id=task.id,
            user_id=task.user_id,
            task_data=task_data,
            is_recurring=task.is_recurring,
            recurrence_rule=task.recurrence_rule,
        )

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


# =============================================================================
# Part B: Advanced Features - Reminder Endpoints
# =============================================================================


@router.get("/reminders/check", response_model=List[dict])
async def check_reminders(
    session: AsyncSession = Depends(get_session),
) -> List[dict]:
    """
    Check for due reminders and return them for processing.

    This endpoint is called by the Dapr cron binding every minute.
    It finds all tasks with reminders due (reminder_at <= now) that
    haven't been sent yet (reminder_sent = False).

    Note: This endpoint does NOT require authentication as it's called
    by the Dapr sidecar. In production, you may want to add IP filtering
    or use Dapr's built-in security features.

    Returns:
        List[dict]: List of due reminders with task info
    """
    from ..models.push_subscription import PushSubscription

    now = _utc_now()

    # Find tasks with due reminders that haven't been sent
    statement = select(Task).where(
        Task.reminder_at.is_not(None),
        Task.reminder_at <= now,
        Task.reminder_sent == False,
        Task.deleted_at.is_(None),
    )
    result = await session.execute(statement)
    due_tasks = result.scalars().all()

    reminders = []
    for task in due_tasks:
        # Get user's push subscriptions
        sub_statement = select(PushSubscription).where(
            PushSubscription.user_id == task.user_id
        )
        sub_result = await session.execute(sub_statement)
        subscriptions = sub_result.scalars().all()

        for subscription in subscriptions:
            reminders.append({
                "task_id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "reminder_at": task.reminder_at.isoformat() if task.reminder_at else None,
                "due_at": task.due_at.isoformat() if task.due_at else None,
                "push_subscription": subscription.to_webpush_dict(),
            })

    return reminders


@router.patch("/{task_id}/reminder-sent", response_model=TaskResponse)
async def mark_reminder_sent(
    task_id: int,
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Mark a task's reminder as sent.

    This endpoint is called by the notification service after
    successfully delivering a reminder notification. It sets
    reminder_sent = True to prevent duplicate notifications.

    Note: This endpoint does NOT require authentication as it's called
    by the notification service. In production, you may want to add
    service-to-service authentication.

    Args:
        task_id: ID of the task to mark

    Returns:
        TaskResponse: Updated task with reminder_sent = True

    Raises:
        HTTPException: 404 if task not found
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.reminder_sent = True
    task.mark_updated()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return await _task_to_response(session, task)


@router.post("/reminders/binding", status_code=status.HTTP_200_OK)
async def handle_cron_binding(
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Handle Dapr cron binding trigger for reminder checks.

    Dapr calls this endpoint based on the cron schedule configured
    in the reminder-cron binding component. This endpoint:
    1. Checks for due reminders
    2. Publishes reminder events to Kafka for each due reminder
    3. Returns status

    Returns:
        dict: Status with count of reminders published
    """
    from ..dapr_client import publish_reminder_event
    from ..models.push_subscription import PushSubscription

    now = _utc_now()

    # Find tasks with due reminders
    statement = select(Task).where(
        Task.reminder_at.is_not(None),
        Task.reminder_at <= now,
        Task.reminder_sent == False,
        Task.deleted_at.is_(None),
    )
    result = await session.execute(statement)
    due_tasks = result.scalars().all()

    published_count = 0
    for task in due_tasks:
        # Get user's push subscriptions
        sub_statement = select(PushSubscription).where(
            PushSubscription.user_id == task.user_id
        )
        sub_result = await session.execute(sub_statement)
        subscriptions = sub_result.scalars().all()

        for subscription in subscriptions:
            success = await publish_reminder_event(
                task_id=task.id,
                user_id=task.user_id,
                title=task.title,
                reminder_at=task.reminder_at,
                due_at=task.due_at,
                push_subscription=subscription.to_webpush_dict(),
            )
            if success:
                published_count += 1

    return {"status": "ok", "reminders_published": published_count}
