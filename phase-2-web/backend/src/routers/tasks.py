"""
Task CRUD endpoints for the API.

This module provides RESTful endpoints for managing tasks with user authentication.
All endpoints require a valid JWT token and automatically filter tasks by user_id.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List

from ..database import get_session
from ..auth import get_current_user
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> List[Task]:
    """
    List all tasks for the authenticated user.

    Args:
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        List[Task]: User's tasks ordered by created_at descending (newest first)
    """
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    result = await session.execute(statement)
    tasks = result.scalars().all()
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title and optional description)
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Task: The newly created task

    Raises:
        HTTPException: 422 if validation fails
    """
    # Validation is handled by Pydantic TaskCreate schema
    # - title: 1-200 characters (required)
    # - description: max 1000 characters (optional)

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID to retrieve
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Task: The requested task

    Raises:
        HTTPException: 404 if task not found, 403 if user doesn't own the task
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Update a task's title or description.

    Args:
        task_id: Task ID to update
        task_data: Updated task data (title, description)
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Task: The updated task

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
        setattr(task, field, value)

    task.mark_updated()  # Update the updated_at timestamp
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Toggle the completion status of a task.

    Args:
        task_id: ID of the task to toggle
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Task: Updated task with toggled completion status

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
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> None:
    """
    Delete a task.

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

    await session.delete(task)
    await session.commit()
