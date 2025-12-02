# Phase 2: Full-Stack Web Todo Application

## Project Overview

This is Phase 2 of the Evolution of Todo hackathon project. It transforms the Phase 1 console app into a multi-user full-stack web application.

## Architecture

- **Frontend**: Next.js 16 with App Router, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI with SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (frontend) with JWT verification (backend)

## Directory Structure

```
phase-2-web/
├── frontend/          # Next.js 16 App
│   ├── src/app/       # App Router pages
│   ├── src/components/# React components
│   ├── src/lib/       # Utilities (auth, api, db)
│   └── drizzle/       # Database schema
├── backend/           # FastAPI App
│   ├── src/           # Source code
│   │   ├── models/    # SQLModel models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── routers/   # API routes
│   └── tests/         # pytest tests
└── docker-compose.yml
```

## Development

### Frontend
```bash
cd frontend
pnpm install
pnpm dev  # http://localhost:3000
```

### Backend
```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn src.main:app --reload --port 8000
```

## Key Patterns

### Next.js 16
- Use `proxy.ts` for auth protection (NOT middleware.ts)
- Dynamic route params are Promises: `params: Promise<{ id: string }>`
- Server Components for data fetching, Client Components for interactivity

### Authentication Flow
1. User logs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend sends JWT to FastAPI backend
4. Backend verifies JWT via JWKS endpoint
5. User ID extracted from JWT `sub` claim

### API Endpoints (Backend)
- `GET /api/health` - Health check
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle completion

## Testing

### Backend
```bash
cd backend
pytest -v
pytest --cov=src
```

## Environment Variables

See `.env.example` files in both frontend and backend directories.
