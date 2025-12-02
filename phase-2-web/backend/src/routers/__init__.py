"""
API routers module.

This module exports all API routers for inclusion in the main application.
"""

from .tasks import router as tasks_router

__all__ = ["tasks_router"]
