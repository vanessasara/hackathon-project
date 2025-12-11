"""
Tests for the health check endpoint.
"""


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"


def test_auth_headers_fixture(auth_headers):
    """Test the auth_headers fixture."""
    assert "Authorization" in auth_headers
    assert auth_headers["Authorization"] == "Bearer mock-token"
