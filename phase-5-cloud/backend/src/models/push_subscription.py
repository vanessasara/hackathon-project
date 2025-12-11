"""
PushSubscription SQLModel for browser push notification subscriptions.

Part B: Advanced Features - Notifications
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime (without timezone info)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class PushSubscription(SQLModel, table=True):
    """
    Browser push notification subscription.

    Stores Web Push API subscriptions for delivering task reminders
    to users' browsers even when the tab is closed.

    Attributes:
        id: Primary key, auto-generated
        user_id: Reference to the user who owns this subscription (from Better Auth)
        endpoint: Push service endpoint URL (unique per browser)
        p256dh_key: User's public key for encrypting notification payload
        auth_key: Authentication secret for the subscription
        user_agent: Browser user agent string (for debugging)
        created_at: Timestamp when subscription was created
        updated_at: Timestamp when subscription was last updated
    """

    __tablename__ = "push_subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="User ID from Better Auth")
    endpoint: str = Field(description="Push service endpoint URL")
    p256dh_key: str = Field(description="User's public key for encryption (base64)")
    auth_key: str = Field(description="Authentication secret (base64)")
    user_agent: Optional[str] = Field(
        default=None, max_length=500, description="Browser user agent for debugging"
    )
    created_at: datetime = Field(
        default_factory=_utc_now,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=_utc_now,
        description="Last update timestamp",
    )

    def mark_updated(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = _utc_now()

    def to_webpush_dict(self) -> dict:
        """
        Convert subscription to format expected by pywebpush library.

        Returns:
            dict with endpoint and keys for pywebpush.webpush()
        """
        return {
            "endpoint": self.endpoint,
            "keys": {
                "p256dh": self.p256dh_key,
                "auth": self.auth_key,
            },
        }
