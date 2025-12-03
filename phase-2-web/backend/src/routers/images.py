"""
Image upload/delete endpoints for the API.

This module provides endpoints for managing task images with R2 storage.
All endpoints require a valid JWT token and validate task ownership.
"""

import io
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..auth import get_current_user
from ..database import get_session
from ..models.task import Task
from ..models.task_image import TaskImage
from ..schemas.image import ImageResponse
from ..services.r2 import r2_service

router = APIRouter(prefix="/images", tags=["images"])

# Configuration
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGES_PER_TASK = 10
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


async def _verify_task_ownership(
    task_id: int, user_id: str, session: AsyncSession
) -> Task:
    """Verify user owns the task, return task if valid."""
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task


def _get_image_dimensions(file_bytes: bytes) -> tuple[int | None, int | None]:
    """Extract image dimensions using PIL."""
    try:
        with Image.open(io.BytesIO(file_bytes)) as img:
            return img.width, img.height
    except Exception:
        return None, None


@router.post(
    "/tasks/{task_id}/images",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
    task_id: int,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ImageResponse:
    """
    Upload an image to a task.

    Args:
        task_id: Task ID to attach image to
        file: Image file (multipart/form-data)
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        ImageResponse: The uploaded image metadata

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized,
                      400 if file too large or invalid type,
                      409 if max images reached
    """
    # Verify task ownership
    await _verify_task_ownership(task_id, user_id, session)

    # Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_MIME_TYPES)}",
        )

    # Read file content
    file_bytes = await file.read()

    # Validate file size
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024 * 1024)}MB",
        )

    # Check image count for task
    stmt = select(TaskImage).where(TaskImage.task_id == task_id)
    result = await session.execute(stmt)
    existing_images = result.scalars().all()
    if len(existing_images) >= MAX_IMAGES_PER_TASK:
        raise HTTPException(
            status_code=409,
            detail=f"Maximum {MAX_IMAGES_PER_TASK} images per task",
        )

    # Get image dimensions
    width, height = _get_image_dimensions(file_bytes)

    # Generate storage key
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    storage_key = f"{user_id}/{task_id}/{uuid.uuid4()}.{ext}"

    # Upload to R2
    try:
        url = r2_service.upload(file_bytes, storage_key, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    # Create database record
    task_image = TaskImage(
        task_id=task_id,
        user_id=user_id,
        filename=file.filename or "image",
        storage_key=storage_key,
        url=url,
        size_bytes=len(file_bytes),
        mime_type=file.content_type,
        width=width,
        height=height,
    )
    session.add(task_image)
    await session.commit()
    await session.refresh(task_image)

    return ImageResponse(
        id=task_image.id,
        task_id=task_image.task_id,
        filename=task_image.filename,
        url=task_image.url,
        size_bytes=task_image.size_bytes,
        mime_type=task_image.mime_type,
        width=task_image.width,
        height=task_image.height,
        created_at=task_image.created_at,
    )


@router.get("/tasks/{task_id}/images", response_model=List[ImageResponse])
async def list_task_images(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[ImageResponse]:
    """
    List all images for a task.

    Args:
        task_id: Task ID to get images for
        user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        List[ImageResponse]: Images attached to the task

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    # Verify task ownership
    await _verify_task_ownership(task_id, user_id, session)

    # Get images
    stmt = select(TaskImage).where(TaskImage.task_id == task_id).order_by(TaskImage.created_at)
    result = await session.execute(stmt)
    images = result.scalars().all()

    return [
        ImageResponse(
            id=img.id,
            task_id=img.task_id,
            filename=img.filename,
            url=img.url,
            size_bytes=img.size_bytes,
            mime_type=img.mime_type,
            width=img.width,
            height=img.height,
            created_at=img.created_at,
        )
        for img in images
    ]


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete an image.

    Args:
        image_id: Image ID to delete
        user_id: User ID extracted from JWT token
        session: Database session

    Raises:
        HTTPException: 404 if image not found, 403 if not authorized
    """
    # Get image
    image = await session.get(TaskImage, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if image.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this image")

    # Delete from R2
    try:
        r2_service.delete(image.storage_key)
    except Exception:
        # Log error but continue with database deletion
        pass

    # Delete from database
    await session.delete(image)
    await session.commit()
