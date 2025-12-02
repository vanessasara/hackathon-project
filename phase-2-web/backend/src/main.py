"""
FastAPI main application entry point.

This module creates and configures the FastAPI application with CORS middleware
and core endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import tasks_router

app = FastAPI(
    title="Todo API",
    description="FastAPI backend for Evolution of Todo Phase 2",
    version="0.1.0",
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


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status and version information
    """
    return {"status": "healthy", "version": "0.1.0"}
