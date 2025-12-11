"""
Pydantic schemas for Push Subscription API request/response validation.

Part B: Advanced Features - Notifications
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PushSubscriptionCreate(BaseModel):
    """
    Schema for registering a browser push subscription.

    This data comes from the browser's PushManager.subscribe() method.
    The frontend sends this to the backend after the user grants
    notification permission.

    Attributes:
        endpoint: The push service URL provided by the browser
        p256dh_key: The client's public key for encryption (base64)
        auth_key: The authentication secret (base64)
        user_agent: Optional browser user agent for debugging
    """

    endpoint: str = Field(..., description="Push service endpoint URL")
    p256dh_key: str = Field(..., description="Client public key (base64)")
    auth_key: str = Field(..., description="Authentication secret (base64)")
    user_agent: Optional[str] = Field(
        default=None, max_length=500, description="Browser user agent"
    )


class PushSubscriptionResponse(BaseModel):
    """
    Schema for push subscription responses.

    Attributes:
        id: Subscription ID
        user_id: Owner's user ID
        endpoint: Push service endpoint URL
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int
    user_id: str
    endpoint: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class PushSubscriptionDelete(BaseModel):
    """
    Schema for deleting a push subscription.

    Attributes:
        endpoint: The endpoint URL to delete (unique per user)
    """

    endpoint: str = Field(..., description="Push service endpoint URL to delete")
