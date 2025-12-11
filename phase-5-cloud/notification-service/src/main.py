"""
FastAPI main application for Notification Service.

Part B: Advanced Features - Notifications

This service consumes events from Kafka via Dapr pub/sub and sends
browser push notifications for task reminders.
"""

import logging
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .config import settings
from .handlers import handle_reminder_event, handle_task_event

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notification Service",
    description="Handles push notifications for Todo App task reminders",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "notification"}


@app.get("/dapr/subscribe")
async def dapr_subscribe():
    """
    Dapr subscription configuration endpoint.

    Dapr calls this endpoint on startup to discover which topics
    this service subscribes to and which routes handle each topic.

    Returns:
        List of subscription configurations
    """
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/events/reminders",
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task-events",
        },
    ]


@app.post("/events/reminders")
async def handle_reminders_topic(request: Request):
    """
    Handle events from the reminders Kafka topic.

    Dapr delivers CloudEvents to this endpoint when messages
    arrive on the reminders topic.

    Args:
        request: FastAPI request containing CloudEvent data

    Returns:
        JSONResponse with status
    """
    try:
        # Parse CloudEvent envelope
        cloud_event = await request.json()
        logger.debug(f"Received reminder event: {cloud_event}")

        # Extract data from CloudEvent
        event_data: Dict[str, Any] = cloud_event.get("data", {})

        # Handle the reminder
        success = await handle_reminder_event(event_data)

        if success:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "SUCCESS"},
            )
        else:
            # Return success to avoid redelivery for non-retryable failures
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "RETRY"},
            )

    except Exception as e:
        logger.exception(f"Error processing reminder event: {e}")
        # Return 200 to prevent infinite redelivery
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "DROP", "error": str(e)},
        )


@app.post("/events/task-events")
async def handle_task_events_topic(request: Request):
    """
    Handle events from the task-events Kafka topic.

    Processes task lifecycle events (created, updated, completed, deleted).

    Args:
        request: FastAPI request containing CloudEvent data

    Returns:
        JSONResponse with status
    """
    try:
        cloud_event = await request.json()
        logger.debug(f"Received task event: {cloud_event}")

        event_data: Dict[str, Any] = cloud_event.get("data", {})
        success = await handle_task_event(event_data)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "SUCCESS" if success else "DROP"},
        )

    except Exception as e:
        logger.exception(f"Error processing task event: {e}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "DROP", "error": str(e)},
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
