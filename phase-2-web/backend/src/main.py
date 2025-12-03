"""
FastAPI main application entry point.

This module creates and configures the FastAPI application with CORS middleware
and core endpoints.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import tasks_router, labels_router, images_router

# Import all models to ensure they're registered with SQLModel
from .models import Task, Label, TaskLabel, TaskImage  # noqa: F401


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


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status and version information
    """
    return {"status": "healthy", "version": "0.1.0"}
