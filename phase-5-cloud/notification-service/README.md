# Notification Service

Push notification microservice for the Todo App. Consumes Kafka events via Dapr and sends browser push notifications.

## Setup

```bash
uv sync
uv run python generate_vapid.py  # Generate VAPID keys
uv run uvicorn src.main:app --reload --port 8001
```

## Environment Variables

- `VAPID_PUBLIC_KEY` - Web Push public key
- `VAPID_PRIVATE_KEY` - Web Push private key
- `VAPID_SUBJECT` - Contact email for VAPID
- `BACKEND_URL` - Backend API URL
