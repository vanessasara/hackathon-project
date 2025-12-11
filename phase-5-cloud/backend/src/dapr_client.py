"""
Dapr client utility for pub/sub and service invocation.

Part B: Advanced Features - Event-Driven Architecture
"""

import httpx
import logging
from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime

from .config import settings

logger = logging.getLogger(__name__)

# Dapr sidecar HTTP port (default: 3500)
DAPR_HTTP_PORT = 3500
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"

# Pub/Sub component name (must match Dapr component metadata name)
PUBSUB_NAME = "kafka-pubsub"

# Topic names
TOPIC_TASK_EVENTS = "task-events"
TOPIC_REMINDERS = "reminders"
TOPIC_TASK_UPDATES = "task-updates"


class TaskEvent(BaseModel):
    """Event published when task is created, updated, completed, or deleted."""

    event_type: str  # "created" | "updated" | "completed" | "deleted"
    task_id: int
    user_id: str
    task_data: dict
    timestamp: datetime
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None


class ReminderEvent(BaseModel):
    """Event published when a task reminder is due for delivery."""

    task_id: int
    user_id: str
    title: str
    reminder_at: datetime
    due_at: Optional[datetime] = None
    push_subscription: Optional[dict] = None  # endpoint, keys


async def publish_event(topic: str, data: dict) -> bool:
    """
    Publish an event to a Kafka topic via Dapr pub/sub.

    Args:
        topic: Topic name to publish to
        data: Event data (will be JSON serialized)

    Returns:
        bool: True if published successfully, False otherwise
    """
    url = f"{DAPR_BASE_URL}/v1.0/publish/{PUBSUB_NAME}/{topic}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10.0,
            )

            if response.status_code == 204:
                logger.info(f"Published event to {topic}: {data.get('event_type', 'unknown')}")
                return True
            else:
                logger.error(
                    f"Failed to publish to {topic}: {response.status_code} - {response.text}"
                )
                return False

    except httpx.RequestError as e:
        logger.error(f"Dapr publish request failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error publishing to Dapr: {e}")
        return False


async def publish_task_event(
    event_type: str,
    task_id: int,
    user_id: str,
    task_data: dict,
    is_recurring: bool = False,
    recurrence_rule: Optional[str] = None,
) -> bool:
    """
    Publish a task event to the task-events topic.

    Args:
        event_type: Type of event (created, updated, completed, deleted)
        task_id: ID of the task
        user_id: ID of the user who owns the task
        task_data: Full task data dictionary
        is_recurring: Whether this is a recurring task
        recurrence_rule: The recurrence pattern if applicable

    Returns:
        bool: True if published successfully
    """
    event = TaskEvent(
        event_type=event_type,
        task_id=task_id,
        user_id=user_id,
        task_data=task_data,
        timestamp=datetime.utcnow(),
        is_recurring=is_recurring,
        recurrence_rule=recurrence_rule,
    )

    return await publish_event(TOPIC_TASK_EVENTS, event.model_dump(mode="json"))


async def publish_reminder_event(
    task_id: int,
    user_id: str,
    title: str,
    reminder_at: datetime,
    due_at: Optional[datetime] = None,
    push_subscription: Optional[dict] = None,
) -> bool:
    """
    Publish a reminder event to the reminders topic.

    Args:
        task_id: ID of the task with the reminder
        user_id: ID of the user to notify
        title: Task title for the notification
        reminder_at: When the reminder was scheduled
        due_at: Optional task deadline
        push_subscription: Browser push subscription data

    Returns:
        bool: True if published successfully
    """
    event = ReminderEvent(
        task_id=task_id,
        user_id=user_id,
        title=title,
        reminder_at=reminder_at,
        due_at=due_at,
        push_subscription=push_subscription,
    )

    return await publish_event(TOPIC_REMINDERS, event.model_dump(mode="json"))


async def invoke_service(app_id: str, method: str, data: Optional[dict] = None) -> Optional[Any]:
    """
    Invoke another service via Dapr service invocation.

    Args:
        app_id: Dapr app ID of the target service
        method: HTTP method path to invoke
        data: Optional request body

    Returns:
        Response data if successful, None otherwise
    """
    url = f"{DAPR_BASE_URL}/v1.0/invoke/{app_id}/method/{method}"

    try:
        async with httpx.AsyncClient() as client:
            if data:
                response = await client.post(url, json=data, timeout=30.0)
            else:
                response = await client.get(url, timeout=30.0)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"Service invocation failed: {app_id}/{method} - {response.status_code}"
                )
                return None

    except httpx.RequestError as e:
        logger.error(f"Service invocation request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in service invocation: {e}")
        return None


def is_dapr_enabled() -> bool:
    """
    Check if Dapr sidecar is available.

    Returns:
        bool: True if Dapr is running, False otherwise
    """
    try:
        import httpx

        response = httpx.get(f"{DAPR_BASE_URL}/v1.0/healthz", timeout=2.0)
        return response.status_code == 204
    except Exception:
        return False
