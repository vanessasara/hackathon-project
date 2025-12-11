"""
FastAPI main application entry point.

This module creates and configures the FastAPI application with CORS middleware
and core endpoints.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import (
    tasks_router,
    labels_router,
    images_router,
    chat_router,
    chatkit_router,
    push_subscriptions_router,  # Part B: Advanced Features
)

# Import all models to ensure they're registered with SQLModel
from .models import Task, Label, TaskLabel, TaskImage, Conversation, Message, PushSubscription  # noqa: F401

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - runs on startup and shutdown."""
    # Startup: Create database tables
    await init_db()
    yield
    # Shutdown: Nothing to clean up


app = FastAPI(
    title="Todo API",
    description="FastAPI backend for Evolution of Todo Phase 2",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router, prefix="/api")
app.include_router(labels_router, prefix="/api")
app.include_router(images_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(chatkit_router)  # ChatKit router has its own prefix
app.include_router(push_subscriptions_router, prefix="/api")  # Part B: Advanced Features


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status and version information
    """
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/reminder-cron")
async def handle_reminder_cron():
    """
    Dapr cron binding endpoint for reminder checks.

    Dapr calls this endpoint based on the cron schedule configured
    in the reminder-cron binding component. This endpoint:
    1. Checks for due reminders
    2. Publishes reminder events to Kafka for each due reminder
    3. Returns status
    """
    from datetime import datetime
    from sqlmodel import select
    from .database import get_session
    from .models import Task
    from .models.push_subscription import PushSubscription
    from .dapr_client import publish_reminder_event

    async for session in get_session():
        # Use naive datetime for comparison with database (stored as TIMESTAMP WITHOUT TIME ZONE)
        now = datetime.utcnow()

        # Find tasks with due reminders
        statement = select(Task).where(
            Task.reminder_at.is_not(None),
            Task.reminder_at <= now,
            Task.reminder_sent == False,
            Task.deleted_at.is_(None),
        )
        result = await session.execute(statement)
        due_tasks = result.scalars().all()

        published_count = 0
        for task in due_tasks:
            # Get user's push subscriptions
            sub_statement = select(PushSubscription).where(
                PushSubscription.user_id == task.user_id
            )
            sub_result = await session.execute(sub_statement)
            subscriptions = sub_result.scalars().all()

            for subscription in subscriptions:
                success = await publish_reminder_event(
                    task_id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    reminder_at=task.reminder_at,
                    due_at=task.due_at,
                    push_subscription=subscription.to_webpush_dict(),
                )
                if success:
                    published_count += 1

        logging.info(f"Reminder cron: checked {len(due_tasks)} due tasks, published {published_count} reminders")
        return {"status": "ok", "reminders_published": published_count}
