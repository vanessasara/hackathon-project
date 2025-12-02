# Quickstart: Full-Stack Web Todo Application

**Feature**: 002-fullstack-web-app
**Date**: 2025-12-02

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.13+ (for backend)
- pnpm, npm, yarn, or bun (frontend package manager)
- uv or pip (Python package manager)
- Neon PostgreSQL account (free tier)

## 1. Database Setup (Neon)

1. Create account at [console.neon.tech](https://console.neon.tech)
2. Create a new project named `evolution-of-todo`
3. Copy the connection string (pooled version recommended)

```env
DATABASE_URL=postgresql://user:password@ep-xxx-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## 2. Environment Variables

### Frontend (.env.local)

```env
# Database
DATABASE_URL=postgresql://...

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://...

# Better Auth (for JWT verification)
BETTER_AUTH_URL=http://localhost:3000
```

## 3. Frontend Setup

```bash
cd phase-2-web/frontend

# Install dependencies
pnpm install

# Generate Better Auth tables
pnpm dlx @better-auth/cli generate

# Run migrations
pnpm dlx drizzle-kit migrate

# Start development server
pnpm dev
```

Frontend runs at: http://localhost:3000

## 4. Backend Setup

```bash
cd phase-2-web/backend

# Create virtual environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv pip install -e ".[dev]"

# Start development server
uvicorn src.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

## 5. Run Both Services

Option A: Two terminals
```bash
# Terminal 1: Frontend
cd phase-2-web/frontend && pnpm dev

# Terminal 2: Backend
cd phase-2-web/backend && uvicorn src.main:app --reload
```

Option B: Docker Compose
```bash
cd phase-2-web
docker-compose up
```

## 6. Verify Setup

### Test Backend Health
```bash
curl http://localhost:8000/api/health
# Expected: {"status":"healthy"}
```

### Test Frontend
1. Open http://localhost:3000
2. Click "Register"
3. Create an account
4. Login and verify dashboard loads

### Test Authentication Flow
1. Register a new user
2. Login with credentials
3. Create a task
4. Verify task appears in list
5. Logout and verify redirect to login

## Project Structure

```
phase-2-web/
├── frontend/              # Next.js 16 App
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities (auth, api)
│   └── drizzle/          # Database schema
│
├── backend/              # FastAPI App
│   ├── src/
│   │   ├── main.py       # App entry
│   │   ├── auth.py       # JWT verification
│   │   ├── models/       # SQLModel models
│   │   └── routers/      # API routes
│   └── tests/            # pytest tests
│
└── docker-compose.yml
```

## Common Commands

### Frontend

```bash
pnpm dev              # Start dev server
pnpm build            # Build for production
pnpm start            # Start production server
pnpm lint             # Run ESLint
pnpm dlx drizzle-kit studio  # Open Drizzle Studio
```

### Backend

```bash
uvicorn src.main:app --reload  # Start dev server
pytest                         # Run tests
pytest -v                      # Verbose tests
pytest --cov                   # With coverage
```

## Troubleshooting

### CORS Errors
- Ensure `NEXT_PUBLIC_API_URL` matches backend URL
- Check CORS middleware in FastAPI allows frontend origin

### JWT Verification Fails
- Verify `BETTER_AUTH_URL` is correct in backend .env
- Check JWKS endpoint is accessible: `curl {BETTER_AUTH_URL}/.well-known/jwks.json`

### Database Connection Fails
- Verify `DATABASE_URL` is correct
- Ensure Neon project is running (not suspended)
- Check SSL mode is enabled (`?sslmode=require`)

### Session Not Persisting
- Check cookies are being set (browser dev tools)
- Verify `BETTER_AUTH_SECRET` is the same in frontend

## Next Steps

After setup verification:
1. Run `/sp.tasks` to generate implementation tasks
2. Follow TDD workflow (Red-Green-Refactor)
3. Use dedicated agents for each phase
