"""
Pytest configuration and fixtures for backend tests.

This module provides shared fixtures for testing the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """
    Create a FastAPI test client.

    Returns:
        TestClient: Test client for making requests to the FastAPI app
    """
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """
    Mock authentication headers for testing.

    Returns:
        dict: Headers with mock Bearer token
    """
    return {"Authorization": "Bearer mock-token"}
