# Implementation Plan: Full-Stack Web Todo Application

**Branch**: `002-fullstack-web-app` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web-app/spec.md`

## Summary

Transform the Phase I console todo application into a multi-user full-stack web application with user authentication, RESTful API, and persistent PostgreSQL storage. The system consists of a Next.js 16 frontend with Better Auth for authentication, a FastAPI backend for business logic and data access, and Neon PostgreSQL for persistent storage.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16+
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16, Better Auth, Tailwind CSS, Drizzle ORM (for direct reads)
- Backend: FastAPI, SQLModel, PyJWT, httpx

**Storage**: Neon Serverless PostgreSQL

**Testing**:
- Frontend: Vitest (if needed)
- Backend: pytest

**Target Platform**: Web (modern browsers - Chrome, Firefox, Safari, Edge last 2 versions)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- Task operations complete in under 2 seconds
- Login and dashboard load in under 5 seconds
- Support 100 concurrent authenticated users

**Constraints**:
- Session validity: 7 days minimum
- Title: 1-200 characters
- Description: max 1000 characters
- Responsive design (mobile and desktop)

**Scale/Scope**:
- MVP for hackathon submission
- Single-tenant multi-user application
- 8 user stories, 15 functional requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Feature spec created via /sp.specify, plan via /sp.plan |
| II. Clean Code | ✅ PASS | Will follow PEP 8 (Python) and ESLint/Prettier (TypeScript) |
| III. Test-First Development | ✅ PASS | pytest for backend, TDD workflow will be followed |
| IV. Single Responsibility | ✅ PASS | Separated frontend/backend, models/routes/services |
| V. Evolutionary Architecture | ✅ PASS | Building on Phase I architecture, adding web layer |
| VI. User Experience First | ✅ PASS | Responsive UI, clear error messages, confirmation dialogs |

**Constitution Notes**:
- Phase II extends Phase I principles to web development
- TypeScript/Next.js follows equivalent Clean Code principles (ESLint, Prettier)
- Backend maintains Python TDD practices from Phase I

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web-app/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # API contracts
│   └── api.yaml         # OpenAPI specification
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
phase-2-web/
├── frontend/                    # Next.js 16 Application
│   ├── src/
│   │   ├── app/                # App Router
│   │   │   ├── layout.tsx      # Root layout with providers
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── proxy.ts        # Auth proxy (replaces middleware)
│   │   │   ├── (auth)/         # Auth route group
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── register/
│   │   │   │       └── page.tsx
│   │   │   ├── (dashboard)/    # Protected route group
│   │   │   │   ├── layout.tsx
│   │   │   │   └── page.tsx    # Task list dashboard
│   │   │   └── api/
│   │   │       └── auth/
│   │   │           └── [...all]/
│   │   │               └── route.ts  # Better Auth handler
│   │   ├── components/         # React components
│   │   │   ├── ui/            # Reusable UI components
│   │   │   ├── task-list.tsx
│   │   │   ├── task-item.tsx
│   │   │   ├── task-form.tsx
│   │   │   └── auth-forms.tsx
│   │   ├── lib/               # Utilities
│   │   │   ├── auth.ts        # Better Auth server config
│   │   │   ├── auth-client.ts # Better Auth client
│   │   │   ├── api.ts         # FastAPI client
│   │   │   └── db.ts          # Drizzle client (for direct reads)
│   │   └── types/             # TypeScript types
│   │       └── index.ts
│   ├── drizzle/               # Drizzle schema (for auth tables)
│   │   └── schema.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── drizzle.config.ts
│   └── CLAUDE.md
│
├── backend/                    # FastAPI Application
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry
│   │   ├── config.py          # Settings
│   │   ├── database.py        # SQLModel + Neon connection
│   │   ├── auth.py            # JWT verification
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── task.py        # Task SQLModel
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── task.py        # Pydantic schemas
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── tasks.py       # Task CRUD routes
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── pyproject.toml
│   └── CLAUDE.md
│
├── .env.example               # Environment template
├── docker-compose.yml         # Local development
├── CLAUDE.md                  # Root instructions
└── README.md
```

**Structure Decision**: Web application structure with separate frontend (Next.js) and backend (FastAPI) directories. This separation enables:
- Independent deployment (Vercel for frontend, Railway/Render for backend)
- Clear responsibility boundaries
- Technology-specific tooling and testing

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AUTHENTICATION FLOW                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. User submits login form                                              │
│     ┌─────────┐         ┌─────────────────┐         ┌──────────────┐   │
│     │ Browser │ ──────► │ Next.js App     │ ──────► │ Better Auth  │   │
│     └─────────┘         │ (API Route)     │         │ (validates)  │   │
│                         └─────────────────┘         └──────┬───────┘   │
│                                                            │            │
│  2. Better Auth creates session + issues JWT               │            │
│     ┌─────────┐         ┌─────────────────┐         ┌──────▼───────┐   │
│     │ Browser │ ◄────── │ Set Cookie      │ ◄────── │ Session +    │   │
│     │ (cookie)│         │ + JWT Token     │         │ JWT Created  │   │
│     └─────────┘         └─────────────────┘         └──────────────┘   │
│                                                                          │
│  3. Frontend calls FastAPI with JWT                                      │
│     ┌─────────┐         ┌─────────────────┐         ┌──────────────┐   │
│     │ Browser │ ──────► │ authClient      │ ──────► │ FastAPI      │   │
│     │         │         │ .token()        │   JWT   │ Backend      │   │
│     └─────────┘         └─────────────────┘  Header └──────┬───────┘   │
│                                                            │            │
│  4. FastAPI verifies JWT via JWKS                          │            │
│     ┌─────────┐         ┌─────────────────┐         ┌──────▼───────┐   │
│     │ Task    │ ◄────── │ User Authorized │ ◄────── │ JWKS Verify  │   │
│     │ Data    │         │ (user_id from   │         │ (from Better │   │
│     └─────────┘         │  JWT sub claim) │         │  Auth server)│   │
│                         └─────────────────┘         └──────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## API Contract Summary

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/*` | Better Auth routes (Next.js) | - |
| GET | `/api/tasks` | List user's tasks | JWT |
| POST | `/api/tasks` | Create task | JWT |
| GET | `/api/tasks/{id}` | Get task by ID | JWT |
| PATCH | `/api/tasks/{id}` | Update task | JWT |
| DELETE | `/api/tasks/{id}` | Delete task | JWT |
| PATCH | `/api/tasks/{id}/complete` | Toggle completion | JWT |

## Agent Assignments

| Phase | Task | Agent |
|-------|------|-------|
| B | Database schema, Neon setup | **database-expert** |
| C | Better Auth + JWT verification | **auth-expert** |
| D | FastAPI routes, testing | **backend-expert** |
| E | Next.js pages, components | **frontend-expert** |
| F | Integration review | **fullstack-architect** |

## Complexity Tracking

> No Constitution violations requiring justification.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Separate frontend/backend | Yes | Clear separation of concerns, independent deployment |
| JWT over sessions | Yes | Stateless backend, easier scaling |
| Drizzle + SQLModel | Yes | Drizzle for TS/Next.js, SQLModel for Python - both type-safe |
| Neon PostgreSQL | Yes | Serverless, free tier, easy branching for development |
