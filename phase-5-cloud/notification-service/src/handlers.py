"""
Event handlers for Dapr pub/sub events.

Part B: Advanced Features - Notifications

This module contains handlers for processing events from Kafka topics
via Dapr pub/sub.
"""

import logging
from typing import Any, Dict

import httpx

from .config import settings
from .push import send_reminder_notification

logger = logging.getLogger(__name__)


async def check_reminder_already_sent(task_id: int) -> bool:
    """Check if reminder was already sent for this task."""
    url = f"{settings.backend_url}/api/tasks/{task_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                task_data = response.json()
                return task_data.get("reminder_sent", False)
    except Exception as e:
        logger.debug(f"Could not check reminder status: {e}")
    return False


async def handle_reminder_event(event_data: Dict[str, Any]) -> bool:
    """
    Handle a reminder event from the reminders topic.

    This handler:
    1. Extracts task and subscription info from the event
    2. Sends a push notification to the user's browser
    3. Calls the backend to mark the reminder as sent

    Args:
        event_data: Event data containing task_id, title, push_subscription, etc.

    Returns:
        bool: True if handled successfully, False otherwise
    """
    task_id = event_data.get("task_id")
    user_id = event_data.get("user_id")
    title = event_data.get("title", "Task Reminder")
    due_at = event_data.get("due_at")
    push_subscription = event_data.get("push_subscription")

    if not task_id or not push_subscription:
        logger.warning(f"Invalid reminder event - missing task_id or subscription: {event_data}")
        return True  # Acknowledge invalid messages to stop retries

    # Skip if reminder was already sent (prevents duplicate notifications from Kafka retries)
    if await check_reminder_already_sent(task_id):
        logger.info(f"Reminder already sent for task {task_id}, skipping")
        return True  # Acknowledge to stop retries

    logger.info(f"Processing reminder for task {task_id}: {title}")

    # Send push notification
    success = send_reminder_notification(
        subscription=push_subscription,
        task_id=task_id,
        title=title,
        due_at=due_at,
    )

    if success:
        # Mark reminder as sent in the backend
        await mark_reminder_sent(task_id)
        logger.info(f"Reminder sent for task {task_id}")
        return True
    else:
        logger.error(f"Failed to send reminder for task {task_id}")
        return False


async def mark_reminder_sent(task_id: int) -> bool:
    """
    Call the backend API to mark a reminder as sent.

    This prevents duplicate notifications by setting reminder_sent = True.

    Args:
        task_id: ID of the task to mark

    Returns:
        bool: True if successfully marked, False otherwise
    """
    url = f"{settings.backend_url}/api/tasks/{task_id}/reminder-sent"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, timeout=10.0)

            if response.status_code == 200:
                logger.info(f"Marked reminder sent for task {task_id}")
                return True
            else:
                logger.error(
                    f"Failed to mark reminder sent: {response.status_code} - {response.text}"
                )
                return False

    except httpx.RequestError as e:
        logger.error(f"Request error marking reminder sent: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error marking reminder sent: {e}")
        return False


async def handle_task_event(event_data: Dict[str, Any]) -> bool:
    """
    Handle a task event from the task-events topic.

    This handler processes task lifecycle events (created, updated, completed, deleted).
    For recurring task completion events, it could trigger the creation of the next
    occurrence (though this is currently handled by the backend).

    Args:
        event_data: Event data containing event_type, task_id, task_data, etc.

    Returns:
        bool: True if handled successfully
    """
    event_type = event_data.get("event_type")
    task_id = event_data.get("task_id")
    is_recurring = event_data.get("is_recurring", False)

    logger.info(f"Processing task event: {event_type} for task {task_id}")

    if event_type == "completed" and is_recurring:
        # Log recurring task completion (backend handles next occurrence creation)
        recurrence_rule = event_data.get("recurrence_rule")
        logger.info(f"Recurring task {task_id} completed (rule: {recurrence_rule})")

    return True
