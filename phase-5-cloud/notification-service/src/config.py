"""
Configuration settings for the Notification Service.

Part B: Advanced Features - Notifications
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # VAPID keys for Web Push
    vapid_public_key: str = ""
    vapid_private_key: str = ""
    vapid_subject: str = "mailto:admin@todo-app.example.com"

    # Backend service URL for marking reminders as sent
    backend_url: str = "http://todo-app-backend:8000"

    # Dapr configuration
    dapr_http_port: int = 3500
    dapr_app_id: str = "todo-app-notification"

    # Service configuration
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
