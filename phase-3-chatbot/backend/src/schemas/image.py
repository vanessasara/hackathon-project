"""
Pydantic schemas for Image API request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ImageResponse(BaseModel):
    """
    Schema for image responses.

    This is the complete representation of a task image returned by the API.

    Attributes:
        id: Image ID
        task_id: Parent task ID
        filename: Original filename
        url: Public URL to access the image
        size_bytes: File size in bytes
        mime_type: MIME type of the image
        width: Image width in pixels (if available)
        height: Image height in pixels (if available)
        created_at: Upload timestamp
    """

    id: int
    task_id: int
    filename: str
    url: str
    size_bytes: int
    mime_type: str
    width: Optional[int]
    height: Optional[int]
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
