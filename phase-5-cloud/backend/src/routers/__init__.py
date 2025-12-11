"""
API routers module.

This module exports all API routers for inclusion in the main application.
"""

from .tasks import router as tasks_router
from .labels import router as labels_router
from .images import router as images_router
from .chat import router as chat_router
from .chatkit import router as chatkit_router
from .push_subscriptions import router as push_subscriptions_router  # Part B

__all__ = [
    "tasks_router",
    "labels_router",
    "images_router",
    "chat_router",
    "chatkit_router",
    "push_subscriptions_router",
]
