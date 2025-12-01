"""Data models for the Todo application.

This module contains the Task dataclass that represents a todo item.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a todo item with title, description, and completion status.

    Attributes:
        id: Unique identifier (auto-generated positive integer).
        title: Short description of the task (1-200 characters, required).
        description: Detailed information (optional, max 1000 characters).
        completed: Whether the task is done (default: False).
        created_at: Timestamp when task was created (auto-set).
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
