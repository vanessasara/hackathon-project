# Tasks: Full-Stack Web Todo Application

**Input**: Design documents from `/specs/002-fullstack-web-app/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/api.yaml ✓, quickstart.md ✓

**Tests**: Backend tests included (pytest specified in plan.md). Frontend tests optional.

**Organization**: Tasks grouped by user story for independent implementation and testing.

**Status**: ✅ ALL 103 TASKS COMPLETED

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story reference (US1-US8)
- File paths use `phase-2-web/` as root (see plan.md structure)

---

## Phase 1: Setup (Shared Infrastructure) ✅

**Purpose**: Project initialization and directory structure
**Agent**: Manual / Any

- [x] T001 Create frontend project with Next.js 16 in phase-2-web/frontend/
- [x] T002 Create backend project with FastAPI in phase-2-web/backend/
- [x] T003 [P] Configure frontend package.json with dependencies (next, better-auth, drizzle-orm, tailwindcss)
- [x] T004 [P] Configure backend pyproject.toml with dependencies (fastapi, sqlmodel, asyncpg, uvicorn)
- [x] T005 [P] Create .env.example files for frontend and backend
- [x] T006 [P] Create CLAUDE.md files (root, frontend, backend) per plan.md
- [x] T007 [P] Configure Tailwind CSS in phase-2-web/frontend/tailwind.config.ts
- [x] T008 [P] Configure TypeScript in phase-2-web/frontend/tsconfig.json
- [x] T009 [P] Configure ESLint and Prettier for frontend

**Checkpoint**: ✅ Project structure ready, dependencies installable

---

## Phase 2: Foundational (Blocking Prerequisites) ✅

**Purpose**: Database, auth framework, and core infrastructure that MUST complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Setup (Agent: database-expert) ✅

- [x] T010 Create Neon PostgreSQL project and obtain connection string
- [x] T011 Configure Drizzle ORM in phase-2-web/frontend/drizzle.config.ts
- [x] T012 Create Drizzle schema for tasks in phase-2-web/frontend/drizzle/schema.ts
- [x] T013 Run Better Auth CLI to generate auth tables schema
- [x] T014 Run Drizzle migrations to create database tables
- [x] T015 Create database client in phase-2-web/frontend/src/lib/db.ts

### Backend Database (Agent: database-expert) ✅

- [x] T016 Create database connection in phase-2-web/backend/src/database.py (async with asyncpg)
- [x] T017 Create Task SQLModel in phase-2-web/backend/src/models/task.py
- [x] T018 Create Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse) in phase-2-web/backend/src/schemas/task.py
- [x] T019 Configure settings/config in phase-2-web/backend/src/config.py

### Authentication Framework (Agent: auth-expert) ✅

- [x] T020 Configure Better Auth server in phase-2-web/frontend/src/lib/auth.ts
- [x] T021 Create Better Auth client in phase-2-web/frontend/src/lib/auth-client.ts
- [x] T022 Create Better Auth API route handler in phase-2-web/frontend/src/app/api/auth/[...all]/route.ts
- [x] T023 Create proxy.ts for auth protection in phase-2-web/frontend/src/app/proxy.ts
- [x] T024 Implement JWT verification in phase-2-web/backend/src/auth.py
- [x] T025 Create get_current_user dependency in phase-2-web/backend/src/auth.py
- [x] T026 Write pytest tests for JWT verification in phase-2-web/backend/tests/test_auth.py

### Backend Core (Agent: backend-expert) ✅

- [x] T027 Create FastAPI main app in phase-2-web/backend/src/main.py
- [x] T028 Configure CORS middleware in phase-2-web/backend/src/main.py
- [x] T029 Create health check endpoint GET /api/health in phase-2-web/backend/src/main.py
- [x] T030 Create pytest conftest.py in phase-2-web/backend/tests/conftest.py

### Frontend Core (Agent: frontend-expert) ✅

- [x] T031 Create root layout with providers in phase-2-web/frontend/src/app/layout.tsx
- [x] T032 Create API client for FastAPI in phase-2-web/frontend/src/lib/api.ts
- [x] T033 Create TypeScript types in phase-2-web/frontend/src/types/index.ts
- [x] T034 [P] Create reusable UI components (Button, Input, Card) in phase-2-web/frontend/src/components/ui/

**Checkpoint**: ✅ Foundation ready - Database connected, auth framework in place, FastAPI running

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP ✅

**Goal**: New users can create accounts with email and password
**Agent**: auth-expert (backend), frontend-expert (UI)

**Independent Test**: Register a new user, verify they can subsequently log in

### Backend Implementation ✅

- [x] T035 [US1] Verify Better Auth handles registration via /api/auth/sign-up endpoint

### Frontend Implementation ✅

- [x] T036 [US1] Create registration page in phase-2-web/frontend/src/app/(auth)/register/page.tsx
- [x] T037 [US1] Create AuthForm component in phase-2-web/frontend/src/components/auth-forms.tsx
- [x] T038 [US1] Add form validation (email format, password min 8 chars)
- [x] T039 [US1] Add error display for duplicate email, validation errors
- [x] T040 [US1] Add redirect to dashboard on successful registration

**Checkpoint**: ✅ Users can register with email/password, see validation errors, redirect on success

---

## Phase 4: User Story 2 - User Login (Priority: P1) 🎯 MVP ✅

**Goal**: Registered users can authenticate and access their dashboard
**Agent**: auth-expert (backend), frontend-expert (UI)

**Independent Test**: Log in with valid credentials, verify dashboard access

### Backend Implementation ✅

- [x] T041 [US2] Verify Better Auth handles login via /api/auth/sign-in endpoint

### Frontend Implementation ✅

- [x] T042 [US2] Create login page in phase-2-web/frontend/src/app/(auth)/login/page.tsx
- [x] T043 [US2] Add login form using AuthForm component
- [x] T044 [US2] Add error display for invalid credentials
- [x] T045 [US2] Add redirect to dashboard on successful login
- [x] T046 [US2] Add "Register" link on login page

**Checkpoint**: ✅ Users can log in, see auth errors, access dashboard after login

---

## Phase 5: User Story 3 - View Task List (Priority: P1) 🎯 MVP ✅

**Goal**: Authenticated users can see all their tasks on the dashboard
**Agent**: backend-expert (API), frontend-expert (UI)

**Independent Test**: Log in, verify task list displays (or empty state)

### Backend Implementation ✅

- [x] T047 [US3] Create tasks router in phase-2-web/backend/src/routers/tasks.py
- [x] T048 [US3] Implement GET /api/tasks endpoint (list user's tasks)
- [x] T049 [US3] Add user_id filtering to ensure users only see their own tasks
- [x] T050 [US3] Write pytest tests for GET /api/tasks in phase-2-web/backend/tests/test_tasks.py

### Frontend Implementation ✅

- [x] T051 [US3] Create dashboard layout in phase-2-web/frontend/src/app/(dashboard)/layout.tsx
- [x] T052 [US3] Create dashboard page in phase-2-web/frontend/src/app/(dashboard)/page.tsx
- [x] T053 [US3] Create TaskList component in phase-2-web/frontend/src/components/task-list.tsx
- [x] T054 [US3] Create TaskItem component in phase-2-web/frontend/src/components/task-item.tsx
- [x] T055 [US3] Add empty state message when no tasks exist
- [x] T056 [US3] Style task list with Tailwind CSS (responsive)

**Checkpoint**: ✅ Dashboard shows user's tasks or empty state, no other user's tasks visible

---

## Phase 6: User Story 4 - Add New Task (Priority: P2) ✅

**Goal**: Authenticated users can create new tasks
**Agent**: backend-expert (API), frontend-expert (UI)

**Independent Test**: Create a task, verify it appears in the list

### Backend Implementation ✅

- [x] T057 [US4] Implement POST /api/tasks endpoint in phase-2-web/backend/src/routers/tasks.py
- [x] T058 [US4] Add validation for title (1-200 chars) and description (max 1000 chars)
- [x] T059 [US4] Set user_id from authenticated user, set completed=false
- [x] T060 [US4] Write pytest tests for POST /api/tasks in phase-2-web/backend/tests/test_tasks.py

### Frontend Implementation ✅

- [x] T061 [US4] Create TaskForm component in phase-2-web/frontend/src/components/task-form.tsx
- [x] T062 [US4] Add task creation form to dashboard page
- [x] T063 [US4] Add form validation (title required, length limits)
- [x] T064 [US4] Add optimistic UI update or refetch on success
- [x] T065 [US4] Add error handling for failed creation

**Checkpoint**: ✅ Users can add tasks with title and optional description, see them in list

---

## Phase 7: User Story 5 - Update Task (Priority: P2) ✅

**Goal**: Authenticated users can edit task title and description
**Agent**: backend-expert (API), frontend-expert (UI)

**Independent Test**: Edit a task's title, verify change persists

### Backend Implementation ✅

- [x] T066 [US5] Implement GET /api/tasks/{task_id} endpoint
- [x] T067 [US5] Implement PATCH /api/tasks/{task_id} endpoint
- [x] T068 [US5] Add authorization check (user owns the task)
- [x] T069 [US5] Return 403 Forbidden if user doesn't own task
- [x] T070 [US5] Return 404 Not Found if task doesn't exist
- [x] T071 [US5] Write pytest tests for PATCH /api/tasks/{task_id}

### Frontend Implementation ✅

- [x] T072 [US5] Add edit mode to TaskItem component
- [x] T073 [US5] Create inline edit form or modal for editing
- [x] T074 [US5] Add save and cancel actions
- [x] T075 [US5] Add optimistic update or refetch on success

**Checkpoint**: ✅ Users can edit their tasks, changes persist, cannot edit others' tasks

---

## Phase 8: User Story 6 - Mark Task Complete (Priority: P3) ✅

**Goal**: Authenticated users can toggle task completion status
**Agent**: backend-expert (API), frontend-expert (UI)

**Independent Test**: Toggle task completion, verify status changes

### Backend Implementation ✅

- [x] T076 [US6] Implement PATCH /api/tasks/{task_id}/complete endpoint
- [x] T077 [US6] Toggle completed status (true → false, false → true)
- [x] T078 [US6] Add authorization check (user owns the task)
- [x] T079 [US6] Write pytest tests for toggle endpoint

### Frontend Implementation ✅

- [x] T080 [US6] Add checkbox to TaskItem component
- [x] T081 [US6] Handle checkbox click to toggle completion
- [x] T082 [US6] Update UI immediately (optimistic update)
- [x] T083 [US6] Style completed tasks differently (strikethrough, muted)

**Checkpoint**: ✅ Users can toggle completion with single click, visual feedback immediate

---

## Phase 9: User Story 7 - Delete Task (Priority: P3) ✅

**Goal**: Authenticated users can delete tasks with confirmation
**Agent**: backend-expert (API), frontend-expert (UI)

**Independent Test**: Delete a task, verify it's removed from list

### Backend Implementation ✅

- [x] T084 [US7] Implement DELETE /api/tasks/{task_id} endpoint
- [x] T085 [US7] Add authorization check (user owns the task)
- [x] T086 [US7] Return 204 No Content on success
- [x] T087 [US7] Write pytest tests for DELETE endpoint

### Frontend Implementation ✅

- [x] T088 [US7] Add delete button to TaskItem component
- [x] T089 [US7] Add confirmation dialog before deletion
- [x] T090 [US7] Handle cancel to keep task in list
- [x] T091 [US7] Remove task from UI on successful deletion

**Checkpoint**: ✅ Users can delete tasks with confirmation, task disappears from list

---

## Phase 10: User Story 8 - User Logout (Priority: P4) ✅

**Goal**: Authenticated users can securely end their session
**Agent**: auth-expert (backend), frontend-expert (UI)

**Independent Test**: Log out, verify redirect to login and cannot access dashboard

### Implementation ✅

- [x] T092 [US8] Add logout button to dashboard layout header
- [x] T093 [US8] Call Better Auth signOut on click
- [x] T094 [US8] Redirect to login page after logout
- [x] T095 [US8] Verify proxy.ts redirects unauthenticated users to login

**Checkpoint**: ✅ Users can log out, session terminated, redirected to login

---

## Phase 11: Polish & Cross-Cutting Concerns ✅

**Purpose**: Final improvements, integration testing, documentation
**Agent**: fullstack-architect

- [x] T096 [P] Create landing page in phase-2-web/frontend/src/app/page.tsx
- [x] T097 [P] Add responsive design validation (mobile + desktop)
- [x] T098 [P] Run quickstart.md verification steps
- [x] T099 [P] Create docker-compose.yml for local development
- [x] T100 [P] Update root README.md with Phase 2 instructions
- [x] T101 Run end-to-end manual testing of all user stories
- [x] T102 Performance check (operations under 2 seconds)
- [x] T103 Security review (no exposed secrets, proper auth)

**Checkpoint**: ✅ Application production-ready, all user stories verified

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ✅
    ↓
Phase 2: Foundational ✅ ← CRITICAL GATE (blocks all stories)
    ↓
Phase 3-10: User Stories ✅ (can run in priority order or parallel if staffed)
    ↓
Phase 11: Polish ✅
```

### User Story Dependencies

| Story | Depends On | Can Parallel With | Status |
|-------|------------|-------------------|--------|
| US1 (Registration) | Phase 2 | US2 (shared auth forms) | ✅ |
| US2 (Login) | Phase 2 | US1 (shared auth forms) | ✅ |
| US3 (View Tasks) | Phase 2 | Independent | ✅ |
| US4 (Add Task) | US3 (needs list to display) | Independent after US3 | ✅ |
| US5 (Update Task) | US3, US4 (needs tasks to edit) | US6, US7 | ✅ |
| US6 (Mark Complete) | US3, US4 | US5, US7 | ✅ |
| US7 (Delete Task) | US3, US4 | US5, US6 | ✅ |
| US8 (Logout) | US2 | Independent | ✅ |

### Agent Workflow

| Phase | Primary Agent | Supporting Agent | Status |
|-------|---------------|------------------|--------|
| Phase 1 | Any | - | ✅ |
| Phase 2 (DB) | database-expert | - | ✅ |
| Phase 2 (Auth) | auth-expert | - | ✅ |
| Phase 2 (Backend) | backend-expert | - | ✅ |
| Phase 2 (Frontend) | frontend-expert | - | ✅ |
| Phase 3-4 | auth-expert | frontend-expert | ✅ |
| Phase 5-9 | backend-expert | frontend-expert | ✅ |
| Phase 10 | auth-expert | frontend-expert | ✅ |
| Phase 11 | fullstack-architect | - | ✅ |

---

## Task Summary

| Phase | Task Count | Completed | Status |
|-------|------------|-----------|--------|
| Phase 1: Setup | 9 | 9 | ✅ |
| Phase 2: Foundational | 25 | 25 | ✅ |
| Phase 3: US1 Registration | 6 | 6 | ✅ |
| Phase 4: US2 Login | 6 | 6 | ✅ |
| Phase 5: US3 View Tasks | 10 | 10 | ✅ |
| Phase 6: US4 Add Task | 9 | 9 | ✅ |
| Phase 7: US5 Update Task | 10 | 10 | ✅ |
| Phase 8: US6 Mark Complete | 8 | 8 | ✅ |
| Phase 9: US7 Delete Task | 8 | 8 | ✅ |
| Phase 10: US8 Logout | 4 | 4 | ✅ |
| Phase 11: Polish | 8 | 8 | ✅ |
| **Total** | **103** | **103** | **✅** |

---

## Implementation Notes

### Technology Updates
- **Database Driver**: Migrated from `psycopg2-binary` (sync) to `asyncpg` (async) for production-grade performance
- **Backend**: All route handlers use `async def` with `AsyncSession` for non-blocking I/O
- **Tests**: 25 backend tests passing with 94% coverage

### Key Files
- Frontend: Next.js 16 with Better Auth, Drizzle ORM
- Backend: FastAPI with SQLModel, asyncpg, JWT verification
- Database: Neon PostgreSQL (serverless)

---

## Notes

- [P] tasks = different files, no dependencies within that group
- [US#] label maps task to specific user story
- Each user story is independently completable and testable after Phase 2
- pytest tests included for backend API endpoints
- Frontend tests optional (not explicitly required)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

**IMPLEMENTATION COMPLETE** 🎉
