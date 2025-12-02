# Backend: FastAPI Application

## Overview

Python FastAPI backend with SQLModel ORM, JWT verification via Better Auth JWKS, and PostgreSQL database.

## Key Files

- `src/main.py` - FastAPI app entry point
- `src/config.py` - Settings and configuration
- `src/database.py` - SQLModel database connection
- `src/auth.py` - JWT verification and user dependency
- `src/models/task.py` - Task SQLModel
- `src/schemas/task.py` - Pydantic request/response schemas
- `src/routers/tasks.py` - Task CRUD endpoints

## Authentication

JWT tokens from Better Auth are verified using JWKS:

```python
# src/auth.py
async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    # Fetch JWKS from Better Auth
    # Verify JWT signature
    # Return user_id from 'sub' claim
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/health | Health check | No |
| GET | /api/tasks | List user's tasks | Yes |
| POST | /api/tasks | Create task | Yes |
| GET | /api/tasks/{id} | Get task | Yes |
| PATCH | /api/tasks/{id} | Update task | Yes |
| DELETE | /api/tasks/{id} | Delete task | Yes |
| PATCH | /api/tasks/{id}/complete | Toggle complete | Yes |

## Commands

```bash
# Development
uvicorn src.main:app --reload --port 8000

# Testing
pytest -v
pytest --cov=src

# Linting
ruff check src/
ruff format src/
```

## Environment Variables

- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_URL` - Frontend URL for JWKS endpoint
- `FRONTEND_URL` - CORS allowed origin

## SQLModel Patterns

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```
