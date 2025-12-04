"""
Tests for task CRUD endpoints with async support.

These tests verify that the task API endpoints correctly handle user authentication,
data isolation, and CRUD operations with async database sessions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from src.main import app
from src.models.task import Task
from src.auth import get_current_user
from src.database import get_session


# Override dependencies for testing
async def override_get_current_user():
    """Mock get_current_user to return a test user ID."""
    return "test-user-id"


async def override_get_session():
    """Mock get_session to return a mock async session."""
    mock_session = AsyncMock()

    # Mock the execute result chain: execute() -> result -> scalars() -> all()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute = AsyncMock(return_value=mock_result)

    mock_session.get = AsyncMock(return_value=None)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.delete = AsyncMock()
    return mock_session


@pytest.fixture(autouse=True)
def reset_overrides():
    """Reset dependency overrides before and after each test."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestListTasks:
    """Tests for GET /api/tasks endpoint."""

    def test_list_tasks_returns_empty_list(self, client):
        """Test that listing tasks returns an empty list when no tasks exist."""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_returns_user_tasks(self, client):
        """Test that listing tasks returns the authenticated user's tasks."""
        mock_tasks = [
            Task(
                id=1,
                user_id="test-user-id",
                title="Task 1",
                description="First task",
                completed=False,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            Task(
                id=2,
                user_id="test-user-id",
                title="Task 2",
                description="Second task",
                completed=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
        ]

        async def mock_get_session_with_tasks():
            mock_session = AsyncMock()

            # Mock the execute result chain
            mock_result = MagicMock()
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = mock_tasks
            mock_result.scalars.return_value = mock_scalars
            mock_session.execute = AsyncMock(return_value=mock_result)

            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_with_tasks

        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"

    def test_list_tasks_requires_authentication(self, client):
        """Test that listing tasks requires authentication."""
        del app.dependency_overrides[get_current_user]
        response = client.get("/api/tasks")
        assert response.status_code == 401


class TestCreateTask:
    """Tests for POST /api/tasks endpoint."""

    def test_create_task_success(self, client):
        """Test that creating a task with valid data succeeds."""
        async def mock_get_session_for_create():
            mock_session = AsyncMock()
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock(side_effect=lambda task: setattr(task, 'id', 1))
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_for_create

        response = client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["completed"] is False

    def test_create_task_empty_title_fails(self, client):
        """Test that creating a task with empty title fails validation."""
        response = client.post("/api/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_title_too_long_fails(self, client):
        """Test that creating a task with title > 200 chars fails validation."""
        response = client.post("/api/tasks", json={"title": "x" * 201})
        assert response.status_code == 422


class TestGetTask:
    """Tests for GET /api/tasks/{task_id} endpoint."""

    def test_get_task_success(self, client):
        """Test successfully retrieving a task by ID."""
        mock_task = Task(
            id=1,
            user_id="test-user-id",
            title="Test Task",
            description="Test description",
            completed=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        async def mock_get_session_with_task():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=mock_task)
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_with_task

        response = client.get("/api/tasks/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test Task"

    def test_get_task_not_found(self, client):
        """Test getting a task that doesn't exist returns 404."""
        async def mock_get_session_no_task():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=None)
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_no_task

        response = client.get("/api/tasks/999")
        assert response.status_code == 404

    def test_get_task_forbidden(self, client):
        """Test getting a task owned by another user returns 403."""
        mock_task = Task(
            id=1,
            user_id="other-user",
            title="Other User's Task",
            description="This belongs to someone else",
            completed=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        async def mock_get_session_other_user_task():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=mock_task)
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_other_user_task

        response = client.get("/api/tasks/1")
        assert response.status_code == 403


class TestUpdateTask:
    """Tests for PATCH /api/tasks/{task_id} endpoint."""

    def test_update_task_success(self, client):
        """Test successfully updating a task's title and description."""
        mock_task = Task(
            id=1,
            user_id="test-user-id",
            title="Old Title",
            description="Old description",
            completed=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        async def mock_get_session_for_update():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=mock_task)
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_for_update

        response = client.patch(
            "/api/tasks/1",
            json={"title": "Updated Title", "description": "Updated description"}
        )
        assert response.status_code == 200
        assert mock_task.title == "Updated Title"
        assert mock_task.description == "Updated description"


class TestToggleComplete:
    """Tests for PATCH /api/tasks/{task_id}/complete endpoint."""

    def test_toggle_complete_success(self, client):
        """Test that toggling task completion works correctly."""
        mock_task = Task(
            id=1,
            user_id="test-user-id",
            title="Test Task",
            description="Test description",
            completed=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        async def mock_get_session_for_toggle():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=mock_task)
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_for_toggle

        response = client.patch("/api/tasks/1/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True  # Should be toggled from False to True


class TestDeleteTask:
    """Tests for DELETE /api/tasks/{task_id} endpoint."""

    def test_delete_task_success(self, client):
        """Test that deleting a task works correctly."""
        mock_task = Task(
            id=1,
            user_id="test-user-id",
            title="Test Task",
            description="Test description",
            completed=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        async def mock_get_session_for_delete():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=mock_task)
            mock_session.delete = AsyncMock()
            mock_session.commit = AsyncMock()
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_for_delete

        response = client.delete("/api/tasks/1")
        assert response.status_code == 204

    def test_delete_task_not_found(self, client):
        """Test that deleting a non-existent task returns 404."""
        async def mock_get_session_no_task():
            mock_session = AsyncMock()
            mock_session.get = AsyncMock(return_value=None)
            return mock_session

        app.dependency_overrides[get_session] = mock_get_session_no_task

        response = client.delete("/api/tasks/999")
        assert response.status_code == 404
