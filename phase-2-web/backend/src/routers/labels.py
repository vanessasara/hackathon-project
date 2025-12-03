"""
Label CRUD endpoints for the API.

This module provides RESTful endpoints for managing labels with user authentication.
All endpoints require a valid JWT token and automatically filter labels by user_id.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..auth import get_current_user
from ..database import get_session
from ..models.label import Label
from ..models.task_label import TaskLabel
from ..schemas.label import LabelCreate, LabelResponse, LabelUpdate

router = APIRouter(prefix="/labels", tags=["labels"])


@router.get("", response_model=List[LabelResponse])
async def list_labels(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[Label]:
    """
    List all labels for the authenticated user.

    Args:
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        List[Label]: User's labels ordered by name
    """
    statement = select(Label).where(Label.user_id == user_id).order_by(Label.name)
    result = await session.execute(statement)
    labels = result.scalars().all()
    return labels


@router.post("", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
async def create_label(
    label_data: LabelCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Label:
    """
    Create a new label for the authenticated user.

    Args:
        label_data: Label creation data (name)
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Label: The newly created label

    Raises:
        HTTPException: 409 if label with same name exists
    """
    # Check for duplicate name
    existing = await session.execute(
        select(Label).where(Label.user_id == user_id, Label.name == label_data.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Label with this name already exists",
        )

    label = Label(user_id=user_id, name=label_data.name)
    session.add(label)
    await session.commit()
    await session.refresh(label)
    return label


@router.get("/{label_id}", response_model=LabelResponse)
async def get_label(
    label_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Label:
    """
    Get a specific label by ID.

    Args:
        label_id: Label ID to retrieve
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Label: The requested label

    Raises:
        HTTPException: 404 if label not found, 403 if user doesn't own the label
    """
    label = await session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if label.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this label")
    return label


@router.patch("/{label_id}", response_model=LabelResponse)
async def update_label(
    label_id: int,
    label_data: LabelUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Label:
    """
    Update a label's name.

    Args:
        label_id: Label ID to update
        label_data: Updated label data (name)
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Label: The updated label

    Raises:
        HTTPException: 404 if label not found, 403 if not authorized, 409 if name exists
    """
    label = await session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if label.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this label")

    # Check for duplicate name if name is being changed
    if label_data.name and label_data.name != label.name:
        existing = await session.execute(
            select(Label).where(
                Label.user_id == user_id,
                Label.name == label_data.name,
                Label.id != label_id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Label with this name already exists",
            )

    update_data = label_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(label, field, value)

    label.mark_updated()
    session.add(label)
    await session.commit()
    await session.refresh(label)
    return label


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(
    label_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a label and remove it from all tasks.

    Args:
        label_id: ID of the label to delete
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        None: 204 No Content on success

    Raises:
        HTTPException: 404 if label not found, 403 if not authorized
    """
    label = await session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if label.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Remove label from all tasks first
    statement = select(TaskLabel).where(TaskLabel.label_id == label_id)
    result = await session.execute(statement)
    task_labels = result.scalars().all()
    for tl in task_labels:
        await session.delete(tl)

    # Then delete label
    await session.delete(label)
    await session.commit()
