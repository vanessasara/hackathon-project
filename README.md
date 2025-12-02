# Evolution of Todo

A hackathon project demonstrating the evolution of a todo application through multiple phases, from a simple console app to a full-stack web application.

## Phases

### Phase 1: Console Todo App
**Location**: `phase-1-console/` (implemented via `001-console-todo-app/`)

A simple Python console application with in-memory task management.

**Features**:
- Add, list, complete, and delete tasks
- Task persistence in memory (Python dataclass)
- Interactive CLI interface
- Comprehensive test coverage with pytest

**Tech Stack**:
- Python 3.13+
- Standard library only (no external dependencies)
- pytest for testing

### Phase 2: Full-Stack Web Application
**Location**: `phase-2-web/`

A modern, multi-user full-stack web application with authentication and database persistence.

**Features**:
- User registration and authentication
- Multi-user support with isolated task lists
- RESTful API backend
- Responsive web interface
- Full CRUD operations for tasks
- JWT-based authentication

**Tech Stack**:
- **Frontend**: Next.js 16, TypeScript, Tailwind CSS, Better Auth
- **Backend**: FastAPI, Python 3.13, SQLModel
- **Database**: Neon Serverless PostgreSQL
- **ORM**: Drizzle (frontend), SQLModel (backend)

## Quick Start

### Phase 1 - Console App

```bash
cd 001-console-todo-app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python src/main.py
```

### Phase 2 - Web App

See detailed setup in [phase-2-web/CLAUDE.md](phase-2-web/CLAUDE.md)

#### Prerequisites
- Node.js 18+
- Python 3.13+
- pnpm (or npm/yarn)
- Neon PostgreSQL account

#### Environment Setup

1. Create a Neon database at [console.neon.tech](https://console.neon.tech)
2. Copy `.env.example` files in both `frontend/` and `backend/` directories
3. Fill in your database credentials and secrets

#### Development

**Option 1: Run services separately**

```bash
# Terminal 1 - Frontend
cd phase-2-web/frontend
pnpm install
pnpm dev  # http://localhost:3000

# Terminal 2 - Backend
cd phase-2-web/backend
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn src.main:app --reload  # http://localhost:8000
```

**Option 2: Docker Compose**

```bash
cd phase-2-web
docker-compose up
```

## Project Structure

```
evolution-of-todo/
├── 001-console-todo-app/     # Phase 1: Console app
│   ├── src/                  # Source code
│   ├── tests/                # pytest tests
│   └── pyproject.toml        # Dependencies
│
├── phase-2-web/              # Phase 2: Web app
│   ├── frontend/             # Next.js frontend
│   │   ├── src/app/         # App Router pages
│   │   ├── src/components/  # React components
│   │   ├── src/lib/         # Auth, API, DB utilities
│   │   └── drizzle/         # Database schema
│   ├── backend/              # FastAPI backend
│   │   ├── src/             # Source code
│   │   │   ├── models/      # SQLModel models
│   │   │   ├── schemas/     # Pydantic schemas
│   │   │   └── routers/     # API routes
│   │   └── tests/           # pytest tests
│   └── docker-compose.yml    # Docker setup
│
├── specs/                    # Feature specifications
│   ├── 001-console-todo-app/
│   └── 002-fullstack-web-app/
│
└── history/                  # Development history
    ├── prompts/              # Prompt history records
    └── adr/                  # Architecture decision records
```

## Testing

### Phase 1
```bash
cd 001-console-todo-app
pytest -v
pytest --cov=src
```

### Phase 2 Backend
```bash
cd phase-2-web/backend
pytest -v
pytest --cov=src
```

## Documentation

- **Phase 1 Spec**: [specs/001-console-todo-app/spec.md](specs/001-console-todo-app/spec.md)
- **Phase 2 Spec**: [specs/002-fullstack-web-app/spec.md](specs/002-fullstack-web-app/spec.md)
- **Phase 2 Quickstart**: [specs/002-fullstack-web-app/quickstart.md](specs/002-fullstack-web-app/quickstart.md)

## Development Methodology

This project uses Spec-Driven Development (SDD) with:
- Detailed feature specifications
- Architecture decision records (ADRs)
- Prompt history records (PHRs)
- Test-driven development (TDD)
- Dedicated AI agents for each development phase

## License

MIT
