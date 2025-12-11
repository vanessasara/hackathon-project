"""
Web Push notification sender.

Part B: Advanced Features - Notifications

This module handles sending browser push notifications using the Web Push protocol
and pywebpush library.
"""

import json
import logging
from typing import Optional

from pywebpush import webpush, WebPushException

from .config import settings

logger = logging.getLogger(__name__)


def send_push_notification(
    subscription: dict,
    title: str,
    body: str,
    url: Optional[str] = None,
    icon: Optional[str] = None,
    tag: Optional[str] = None,
) -> bool:
    """
    Send a push notification to a browser subscription.

    Args:
        subscription: Browser push subscription dict with endpoint and keys
        title: Notification title
        body: Notification body text
        url: Optional URL to open when notification is clicked
        icon: Optional icon URL for the notification
        tag: Optional tag for grouping notifications

    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    if not settings.vapid_private_key or not settings.vapid_public_key:
        logger.error("VAPID keys not configured - cannot send push notifications")
        return False

    # Build notification payload
    payload = {
        "title": title,
        "body": body,
        "icon": icon or "/icon-192x192.png",
        "badge": "/badge-72x72.png",
        "tag": tag or "todo-reminder",
        "requireInteraction": True,
        "data": {
            "url": url or "/",
        },
    }

    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps(payload),
            vapid_private_key=settings.vapid_private_key,
            vapid_claims={
                "sub": settings.vapid_subject,
            },
        )
        logger.info(f"Push notification sent: {title}")
        return True

    except WebPushException as e:
        logger.error(f"Web push failed: {e}")

        # Handle subscription gone or invalid (user unsubscribed or subscription expired)
        # Check for 410 Gone or 400 Bad Request (stale subscription)
        should_ack = False
        error_str = str(e)

        if hasattr(e, 'response') and e.response is not None:
            status = getattr(e.response, 'status_code', None)
            if status in (400, 410):
                should_ack = True

        # Also check if error codes appear in the exception message
        if "410" in error_str or "400" in error_str:
            should_ack = True

        if should_ack:
            logger.warning(f"Push subscription invalid/expired - acknowledging to stop retries")
            # Return True to acknowledge the message and stop Dapr from retrying
            return True

        return False

    except Exception as e:
        logger.error(f"Unexpected error sending push notification: {e}")
        return False


def send_reminder_notification(
    subscription: dict,
    task_id: int,
    title: str,
    due_at: Optional[str] = None,
) -> bool:
    """
    Send a task reminder push notification.

    Args:
        subscription: Browser push subscription dict
        task_id: ID of the task being reminded
        title: Task title
        due_at: Optional due date/time string

    Returns:
        bool: True if notification was sent successfully
    """
    body = f"Reminder: {title}"
    if due_at:
        body += f"\nDue: {due_at}"

    return send_push_notification(
        subscription=subscription,
        title="Task Reminder",
        body=body,
        url=f"/tasks?highlight={task_id}",
        tag=f"reminder-{task_id}",
    )
