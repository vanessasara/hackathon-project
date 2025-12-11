#!/usr/bin/env python3
"""
Migration script for Part B: Advanced Features

Adds new columns to the tasks table:
- reminder_sent: Boolean flag to prevent duplicate notifications
- due_at: Task deadline (separate from reminder)
- is_recurring: Whether task repeats
- recurrence_rule: Pattern (daily, weekly, monthly, weekdays)
- recurrence_end: When to stop recurring
- parent_task_id: Link to original recurring task

Creates new table:
- push_subscriptions: Browser push notification subscriptions

Usage:
    cd backend
    uv run python migrate_part_b.py
"""

import asyncio
import ssl
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Load settings
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")


def get_async_url(url: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg:// for async driver."""
    url = url.replace("postgresql://", "postgresql+asyncpg://")
    url = url.replace("?sslmode=require", "").replace("&sslmode=require", "")
    return url


# SQL migrations
MIGRATIONS = [
    # Add reminder_sent column
    """
    ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS reminder_sent BOOLEAN DEFAULT FALSE;
    """,
    # Add due_at column
    """
    ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS due_at TIMESTAMP;
    """,
    # Add is_recurring column
    """
    ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;
    """,
    # Add recurrence_rule column
    """
    ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS recurrence_rule VARCHAR(100);
    """,
    # Add recurrence_end column
    """
    ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS recurrence_end TIMESTAMP;
    """,
    # Add parent_task_id column
    """
    ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS parent_task_id INTEGER;
    """,
    # Create indexes for new columns
    """
    CREATE INDEX IF NOT EXISTS ix_tasks_reminder_sent ON tasks(reminder_sent);
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_tasks_due_at ON tasks(due_at);
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_tasks_is_recurring ON tasks(is_recurring);
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_tasks_parent_task_id ON tasks(parent_task_id);
    """,
    # Create push_subscriptions table
    """
    CREATE TABLE IF NOT EXISTS push_subscriptions (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR NOT NULL,
        endpoint TEXT NOT NULL,
        p256dh_key TEXT NOT NULL,
        auth_key TEXT NOT NULL,
        user_agent VARCHAR(500),
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """,
    # Create index on user_id for push_subscriptions
    """
    CREATE INDEX IF NOT EXISTS ix_push_subscriptions_user_id ON push_subscriptions(user_id);
    """,
    # Create unique index on endpoint for push_subscriptions
    """
    CREATE UNIQUE INDEX IF NOT EXISTS ix_push_subscriptions_endpoint ON push_subscriptions(endpoint);
    """,
]


async def run_migrations():
    """Run all migrations."""
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not set in environment")
        return

    print(f"Connecting to database...")

    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    engine = create_async_engine(
        get_async_url(DATABASE_URL),
        echo=True,
        connect_args={"ssl": ssl_context},
    )

    async with engine.begin() as conn:
        print("\n" + "=" * 60)
        print("Running Part B migrations...")
        print("=" * 60 + "\n")

        for i, migration in enumerate(MIGRATIONS, 1):
            try:
                print(f"[{i}/{len(MIGRATIONS)}] Executing migration...")
                await conn.execute(text(migration))
                print(f"    ✓ Success\n")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                    print(f"    ⚠ Already exists, skipping\n")
                else:
                    print(f"    ✗ Error: {e}\n")
                    raise

    print("=" * 60)
    print("All migrations completed successfully!")
    print("=" * 60)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_migrations())
