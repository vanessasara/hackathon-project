"""
TaskImage SQLModel for storing image metadata.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime (without timezone info)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TaskImage(SQLModel, table=True):
    """
    TaskImage model representing an image attached to a task.

    Attributes:
        id: Primary key, auto-generated
        task_id: Reference to the task this image belongs to
        user_id: Reference to the user who owns this image (denormalized)
        filename: Original filename of the uploaded image
        storage_key: Object key in R2 storage
        url: Public URL to access the image
        size_bytes: File size in bytes
        mime_type: MIME type of the image
        width: Image width in pixels
        height: Image height in pixels
        created_at: Timestamp when image was uploaded
    """

    __tablename__ = "task_images"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(
        foreign_key="tasks.id", index=True, description="Task this image belongs to"
    )
    user_id: str = Field(
        index=True, description="User ID (denormalized for fast queries)"
    )

    filename: str = Field(max_length=255, description="Original filename")
    storage_key: str = Field(max_length=500, description="R2 object key")
    url: str = Field(max_length=1000, description="Public URL")

    size_bytes: int = Field(default=0, description="File size in bytes")
    mime_type: str = Field(
        default="image/jpeg", max_length=100, description="MIME type"
    )
    width: Optional[int] = Field(default=None, description="Image width in pixels")
    height: Optional[int] = Field(default=None, description="Image height in pixels")

    created_at: datetime = Field(
        default_factory=_utc_now,
        description="Upload timestamp",
    )
