"""
TaskLabel SQLModel for many-to-many relationship between tasks and labels.
"""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    """Get current UTC time as naive datetime (without timezone info)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TaskLabel(SQLModel, table=True):
    """
    Junction table for many-to-many relationship between tasks and labels.

    Attributes:
        task_id: Foreign key to tasks table
        label_id: Foreign key to labels table
        created_at: Timestamp when association was created
    """

    __tablename__ = "task_labels"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    label_id: int = Field(foreign_key="labels.id", primary_key=True)
    created_at: datetime = Field(
        default_factory=_utc_now,
        description="When the label was assigned to the task",
    )
