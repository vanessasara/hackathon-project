# Notification Service

## Overview

Python FastAPI microservice that consumes Kafka events via Dapr pub/sub and sends browser push notifications for task reminders.

## Architecture

- **Runtime**: Python 3.11 with FastAPI
- **Event Source**: Kafka (Redpanda Cloud) via Dapr pub/sub
- **Notification**: Web Push API with pywebpush

## Key Files

- `src/main.py` - FastAPI app with Dapr subscription endpoints
- `src/config.py` - Settings and configuration
- `src/handlers.py` - Event handlers for Kafka topics
- `src/push.py` - Web Push notification sender

## Dapr Integration

### Subscriptions

The service subscribes to these Kafka topics via Dapr:

| Topic | Route | Purpose |
|-------|-------|---------|
| reminders | /events/reminders | Task reminder notifications |
| task-events | /events/task-events | Task lifecycle events |

### Subscription Discovery

Dapr calls `GET /dapr/subscribe` on startup to discover subscriptions:

```json
[
  {"pubsubname": "kafka-pubsub", "topic": "reminders", "route": "/events/reminders"},
  {"pubsubname": "kafka-pubsub", "topic": "task-events", "route": "/events/task-events"}
]
```

## Event Schemas

### Reminder Event

```json
{
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Morning standup",
  "reminder_at": "2025-12-08T09:00:00Z",
  "due_at": "2025-12-08T09:30:00Z",
  "push_subscription": {
    "endpoint": "https://fcm.googleapis.com/...",
    "keys": {"p256dh": "...", "auth": "..."}
  }
}
```

## Commands

```bash
# Development
cd notification-service
pip install -e ".[dev]"
uvicorn src.main:app --reload --port 8001

# Generate VAPID keys (run once)
python generate_vapid.py

# Testing
pytest -v
pytest --cov=src

# Docker build
docker build -t notification-service .
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| VAPID_PUBLIC_KEY | Web Push public key (base64url) |
| VAPID_PRIVATE_KEY | Web Push private key (base64url) |
| VAPID_SUBJECT | Contact email for VAPID |
| BACKEND_URL | Backend API URL for marking reminders sent |
| DEBUG | Enable debug logging |

## Kubernetes Deployment

Requires Dapr sidecar annotation:

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "todo-app-notification"
  dapr.io/app-port: "8001"
```
