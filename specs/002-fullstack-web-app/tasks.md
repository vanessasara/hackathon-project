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

**PHASE 1-11 COMPLETE** - Phase 12 (UI/UX Enhancement) In Progress

---

## Phase 12: UI/UX Enhancement - Google Keep Style (NEW)

**Purpose**: Transform the basic todo interface into a polished Google Keep-inspired UI
**Added**: 2025-12-03
**Agent**: frontend-expert (UI), backend-expert (API updates)

### 12.1 Setup & Dependencies

- [ ] T104 Install framer-motion and next-themes dependencies
- [ ] T105 Update globals.css with theme CSS variables (light/dark)
- [ ] T106 Create lib/theme-provider.tsx (next-themes wrapper)
- [ ] T107 Update app/layout.tsx to wrap with ThemeProvider
- [ ] T108 Define KEEP_COLORS constant with 12 color palette

**Checkpoint**: Theme infrastructure ready

---

### 12.2 User Story 9 - Dark/Light Theme Toggle (Priority: P1)

**Goal**: Users can switch between dark and light themes
**Independent Test**: Click toggle, verify UI switches themes, preference persists

- [ ] T109 [US9] Create components/theme-toggle.tsx with Sun/Moon icons
- [ ] T110 [US9] Add animated icon rotation on theme change
- [ ] T111 [US9] Add theme toggle to dashboard header
- [ ] T112 [US9] Verify system preference detection works
- [ ] T113 [US9] Verify theme persists in localStorage

**Checkpoint**: Theme toggle functional, preference remembered

---

### 12.3 User Story 10 - Masonry Grid Layout (Priority: P1)

**Goal**: Tasks display in responsive masonry grid (1-5 columns)
**Independent Test**: View dashboard, verify cards in masonry layout, resize window

- [ ] T114 [US10] Update globals.css with masonry grid CSS (column-count)
- [ ] T115 [US10] Create components/masonry-grid.tsx wrapper
- [ ] T116 [US10] Update task-list.tsx to use masonry grid
- [ ] T117 [US10] Create components/view-toggle.tsx (grid/list switch)
- [ ] T118 [US10] Add view toggle to dashboard header
- [ ] T119 [US10] Implement list view alternative (single column)
- [ ] T120 [US10] Test responsive breakpoints (600px, 900px, 1200px, 1500px)

**Checkpoint**: Masonry grid displays tasks, responsive, toggleable to list view

---

### 12.4 User Story 11 - Color-Coded Tasks (Priority: P2)

**Goal**: Users can assign 12 background colors to tasks
**Independent Test**: Create/edit task, select color, verify card background changes

#### Backend Implementation

- [ ] T121 [US11] Add `color` field to Task model (default="default")
- [ ] T122 [US11] Update TaskCreate/TaskUpdate schemas to include color
- [ ] T123 [US11] Update POST /api/tasks to accept color
- [ ] T124 [US11] Update PATCH /api/tasks/{id} to accept color
- [ ] T125 [US11] Write pytest tests for color field
- [ ] T126 [US11] Create database migration for color field

#### Frontend Implementation

- [ ] T127 [US11] Create components/color-picker.tsx (12-color grid)
- [ ] T128 [US11] Add color picker to task form
- [ ] T129 [US11] Update task-item.tsx to display colored background
- [ ] T130 [US11] Apply dark mode color variants when theme is dark
- [ ] T131 [US11] Add color selection animation (scale on select)

**Checkpoint**: Tasks can be colored, colors display correctly in both themes

---

### 12.5 User Story 12 - Expandable Note Input (Priority: P2)

**Goal**: "Take a note..." input expands to reveal title, content, toolbar
**Independent Test**: Click collapsed input, verify expansion with all fields

- [ ] T132 [US12] Create components/expandable-input.tsx
- [ ] T133 [US12] Implement collapsed state ("Take a note..." placeholder)
- [ ] T134 [US12] Implement expanded state (title, content, toolbar)
- [ ] T135 [US12] Add Framer Motion expand/collapse animation
- [ ] T136 [US12] Add click-outside detection to collapse and save
- [ ] T137 [US12] Integrate color picker in expanded toolbar
- [ ] T138 [US12] Replace existing task-form.tsx with expandable-input

**Checkpoint**: Input expands/collapses smoothly, auto-saves on collapse

---

### 12.6 User Story 13 - Pin Tasks to Top (Priority: P3)

**Goal**: Users can pin important tasks to top of list
**Independent Test**: Pin a task, verify it moves to "Pinned" section

#### Backend Implementation

- [ ] T139 [US13] Add `pinned` field to Task model (default=False)
- [ ] T140 [US13] Update TaskCreate/TaskUpdate schemas to include pinned
- [ ] T141 [US13] Update GET /api/tasks to sort pinned first
- [ ] T142 [US13] Update POST/PATCH endpoints to accept pinned
- [ ] T143 [US13] Write pytest tests for pinned field
- [ ] T144 [US13] Create database migration for pinned field

#### Frontend Implementation

- [ ] T145 [US13] Add pin icon button to task card
- [ ] T146 [US13] Update task-list.tsx to show "Pinned" and "Others" sections
- [ ] T147 [US13] Add pin toggle animation (rotate icon)
- [ ] T148 [US13] Implement optimistic UI update for pin toggle

**Checkpoint**: Tasks can be pinned, pinned section displays at top

---

### 12.7 User Story 14 - Task Edit Modal (Priority: P3)

**Goal**: Clicking task opens modal for focused editing
**Independent Test**: Click card, verify modal opens, edit and close

- [ ] T149 [US14] Create components/todo-modal.tsx with backdrop
- [ ] T150 [US14] Add Framer Motion scale animation for modal open/close
- [ ] T151 [US14] Display title, content, timestamp in modal
- [ ] T152 [US14] Add color picker toolbar in modal
- [ ] T153 [US14] Implement Escape key and click-outside to close
- [ ] T154 [US14] Auto-save changes on modal close
- [ ] T155 [US14] Update task-item.tsx to open modal on click

**Checkpoint**: Modal opens/closes smoothly, edits save correctly

---

### 12.8 User Story 15 - Left Sidebar Navigation (Priority: P4)

**Goal**: Persistent sidebar for navigation (Notes, Archive, Trash)
**Independent Test**: View sidebar, click items, verify navigation

- [ ] T156 [US15] Create components/sidebar.tsx
- [ ] T157 [US15] Add navigation items: Notes, Reminders (placeholder), Archive (placeholder), Trash (placeholder)
- [ ] T158 [US15] Style active item with yellow highlight
- [ ] T159 [US15] Add hamburger menu button to header
- [ ] T160 [US15] Implement sidebar collapse/expand animation
- [ ] T161 [US15] Update dashboard layout to include sidebar
- [ ] T162 [US15] Make sidebar collapsible on mobile (overlay mode)

**Checkpoint**: Sidebar displays, collapses on mobile, Notes is active

---

### 12.9 Card Animations & Polish

**Purpose**: Add Framer Motion animations throughout
**Agent**: frontend-expert

- [ ] T163 [P] Add card enter animation (scale + opacity)
- [ ] T164 [P] Add card exit animation (scale + slide)
- [ ] T165 [P] Add card hover effect (lift + shadow)
- [ ] T166 [P] Add AnimatePresence to task list for exit animations
- [ ] T167 [P] Add layout animation for reordering
- [ ] T168 [P] Add loading skeleton animations
- [ ] T169 [P] Add toast notification animations

**Checkpoint**: All animations smooth at 60fps

---

### 12.10 Final Polish & Testing

**Purpose**: Integration, testing, accessibility
**Agent**: fullstack-architect

- [ ] T170 Verify dark mode colors pass WCAG AA contrast
- [ ] T171 Test all features in light mode
- [ ] T172 Test all features in dark mode
- [ ] T173 Test responsive layout on mobile (375px)
- [ ] T174 Test responsive layout on tablet (768px)
- [ ] T175 Test responsive layout on desktop (1440px)
- [ ] T176 Performance check: animations at 60fps
- [ ] T177 Performance check: theme toggle under 100ms
- [ ] T178 Run existing backend tests (ensure no regressions)
- [ ] T179 Manual E2E test of complete workflow

**Checkpoint**: UI/UX enhancement complete, all tests passing

---

## Phase 12 Dependencies

```
12.1 Setup ← Required by all other tasks
    ↓
12.2 Theme Toggle ← Can start after setup
12.3 Masonry Grid ← Can start after setup
    ↓
12.4 Colors ← Requires backend migration
12.5 Expandable Input ← Can parallel with colors
    ↓
12.6 Pinning ← Requires backend migration
12.7 Modal ← Can parallel with pinning
    ↓
12.8 Sidebar ← Can start after layout stable
12.9 Animations ← Can integrate throughout
    ↓
12.10 Polish ← Final step
```

---

## Updated Task Summary

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
| **Phase 12: UI/UX Enhancement** | **76** | **0** | **⏳** |
| **Total** | **179** | **103** | **58%** |

---

## Phase 12 User Story Summary

| Story | Description | Tasks | Priority |
|-------|-------------|-------|----------|
| US9 | Dark/Light Theme Toggle | T109-T113 (5) | P1 |
| US10 | Masonry Grid Layout | T114-T120 (7) | P1 |
| US11 | Color-Coded Tasks | T121-T131 (11) | P2 |
| US12 | Expandable Note Input | T132-T138 (7) | P2 |
| US13 | Pin Tasks to Top | T139-T148 (10) | P3 |
| US14 | Task Edit Modal | T149-T155 (7) | P3 |
| US15 | Left Sidebar Navigation | T156-T162 (7) | P4 |
| - | Card Animations | T163-T169 (7) | - |
| - | Final Polish | T170-T179 (10) | - |

---

## Phase 13: Advanced Features - Trash, Archive, Labels & Reminders (NEW) ✅

**Purpose**: Add Google Keep-inspired organization features
**Added**: 2025-12-03
**Status**: ✅ COMPLETED
**Agent**: backend-expert (API), frontend-expert (UI)

### 13.1 Backend - Task Model Updates ✅

- [x] T180 [US16] Add `deleted_at: Optional[datetime]` field to Task model
- [x] T181 [US17] Add `archived: bool = False` field to Task model
- [x] T182 [US19] Add `reminder_at: Optional[datetime]` field to Task model
- [x] T183 Update Task model indexes (archived, reminder_at)

**Files**: `backend/src/models/task.py`

### 13.2 Backend - Label Model ✅

- [x] T184 [US18] Create Label SQLModel class
- [x] T185 [US18] Create TaskLabel junction table model
- [x] T186 [US18] Update models/__init__.py exports

**Files**: `backend/src/models/label.py`, `backend/src/models/task_label.py`

### 13.3 Backend - Schemas ✅

- [x] T187 [US16-19] Update TaskUpdate schema with archived, reminder_at
- [x] T188 [US16-19] Update TaskResponse schema with deleted_at, archived, reminder_at
- [x] T189 [US18] Create LabelCreate, LabelUpdate, LabelResponse schemas

**Files**: `backend/src/schemas/task.py`, `backend/src/schemas/label.py`

### 13.4 Backend - Tasks Router Updates ✅

- [x] T190 [US16-19] Add `filter` query param (active, trash, archive, reminders)
- [x] T191 [US18] Add `label_id` query param for label filtering
- [x] T192 [US16] Change DELETE to soft delete (sets deleted_at)
- [x] T193 [US16] Create POST `/tasks/{id}/restore` endpoint
- [x] T194 [US16] Create DELETE `/tasks/{id}/permanent` endpoint
- [x] T195 [US16] Create DELETE `/tasks/trash/empty` endpoint
- [x] T196 [US18] Create POST `/tasks/{id}/labels/{label_id}` endpoint
- [x] T197 [US18] Create DELETE `/tasks/{id}/labels/{label_id}` endpoint

**File**: `backend/src/routers/tasks.py`

### 13.5 Backend - Labels Router ✅

- [x] T198 [US18] Create GET `/labels` endpoint (list user's labels)
- [x] T199 [US18] Create POST `/labels` endpoint (create label)
- [x] T200 [US18] Create GET `/labels/{id}` endpoint
- [x] T201 [US18] Create PATCH `/labels/{id}` endpoint
- [x] T202 [US18] Create DELETE `/labels/{id}` endpoint
- [x] T203 [US18] Register labels router in main.py

**Files**: `backend/src/routers/labels.py`, `backend/src/main.py`

### 13.6 Frontend - Types & API ✅

- [x] T204 [US16-19] Add deleted_at, archived, reminder_at to Task type
- [x] T205 [US18] Create Label type
- [x] T206 [US16-19] Create TaskFilter type (active | trash | archive | reminders)
- [x] T207 [US16-19] Update tasksApi.list with filter and label_id params
- [x] T208 [US16] Add tasksApi.restore method
- [x] T209 [US16] Add tasksApi.permanentDelete method
- [x] T210 [US16] Add tasksApi.emptyTrash method
- [x] T211 [US18] Add tasksApi.addLabel, removeLabel methods
- [x] T212 [US18] Create labelsApi with CRUD methods

**Files**: `frontend/src/types/index.ts`, `frontend/src/lib/api.ts`

### 13.7 Frontend - TaskList Updates ✅

- [x] T213 [US16-19] Add filter prop with default "active"
- [x] T214 [US18] Add labelId prop for label filtering
- [x] T215 Add emptyMessage, emptyDescription props
- [x] T216 Add showPinnedSection prop
- [x] T217 Update fetch to use filter and labelId params

**File**: `frontend/src/components/task-list.tsx`

### 13.8 Frontend - TaskCard Updates ✅

- [x] T218 [US16-17] Add usePathname for context detection
- [x] T219 [US17] Add handleArchive, handleUnarchive handlers
- [x] T220 [US16] Add handleRestore, handlePermanentDelete handlers
- [x] T221 [US19] Add handleReminderChange handler
- [x] T222 [US19] Display reminder chip with formatted date
- [x] T223 Implement context-aware toolbar (different actions per route)

**File**: `frontend/src/components/task-card.tsx`

### 13.9 Frontend - Trash Page ✅

- [x] T224 [US16] Create trash page component
- [x] T225 [US16] Add "Empty Trash" button in header
- [x] T226 [US16] Add 7-day warning banner (display only)
- [x] T227 [US16] Use TaskList with filter="trash"

**File**: `frontend/src/app/dashboard/trash/page.tsx`

### 13.10 Frontend - Archive Page ✅

- [x] T228 [US17] Create archive page component
- [x] T229 [US17] Use TaskList with filter="archive"

**File**: `frontend/src/app/dashboard/archive/page.tsx`

### 13.11 Frontend - Reminders Page ✅

- [x] T230 [US19] Create reminders page component
- [x] T231 [US19] Implement custom task fetching
- [x] T232 [US19] Group tasks by "SENT" (past) and "UPCOMING" (future)
- [x] T233 [US19] Display section headers

**File**: `frontend/src/app/dashboard/reminders/page.tsx`

### 13.12 Frontend - Label Filter Page ✅

- [x] T234 [US18] Create dynamic route [labelId]
- [x] T235 [US18] Use Next.js 16 async params pattern
- [x] T236 [US18] Fetch label info for header
- [x] T237 [US18] Use TaskList with labelId filter

**File**: `frontend/src/app/dashboard/labels/[labelId]/page.tsx`

### 13.13 Frontend - EditLabelsModal ✅

- [x] T238 [US18] Create modal with overlay and animation
- [x] T239 [US18] Add "Create new label" input with + button
- [x] T240 [US18] List existing labels
- [x] T241 [US18] Implement inline edit mode for labels
- [x] T242 [US18] Add delete button with confirmation
- [x] T243 [US18] Add Done button to close

**File**: `frontend/src/components/edit-labels-modal.tsx`

### 13.14 Frontend - ReminderPicker ✅

- [x] T244 [US19] Create modal with overlay and animation
- [x] T245 [US19] Add preset options (Today 8PM, Tomorrow 8AM, Next week Monday 8AM)
- [x] T246 [US19] Add "Pick date & time" option for custom
- [x] T247 [US19] Custom picker with date and time inputs
- [x] T248 [US19] Add "Remove reminder" option when reminder exists
- [x] T249 [US19] Save and cancel handlers

**File**: `frontend/src/components/reminder-picker.tsx`

### 13.15 Frontend - Sidebar Updates ✅

- [x] T250 [US18] Add usePathname for active state
- [x] T251 [US18] Fetch and display labels dynamically
- [x] T252 [US18] Add collapsible labels section
- [x] T253 [US18] Add onEditLabels callback prop
- [x] T254 Highlight active route

**File**: `frontend/src/components/sidebar.tsx`

### 13.16 Frontend - Dashboard Client Updates ✅

- [x] T255 [US18] Add editLabelsOpen state
- [x] T256 [US18] Pass onEditLabels to Sidebar
- [x] T257 [US18] Render EditLabelsModal

**File**: `frontend/src/app/dashboard/dashboard-client.tsx`

---

## Phase 13 Checkpoints ✅

**Checkpoint 13.1**: Backend models updated ✅
**Checkpoint 13.2**: Backend routers functional ✅
**Checkpoint 13.3**: Frontend types and API updated ✅
**Checkpoint 13.4**: All 4 routes working (/trash, /archive, /reminders, /labels/[id]) ✅
**Checkpoint 13.5**: EditLabelsModal and ReminderPicker functional ✅
**Checkpoint 13.6**: Context-aware TaskCard actions working ✅

---

## Updated Task Summary (Final)

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
| Phase 12: UI/UX Enhancement | 76 | 76 | ✅ |
| **Phase 13: Advanced Features** | **78** | **78** | **✅** |
| **Total** | **257** | **257** | **100%** |

---

## Phase 13 User Story Summary

| Story | Description | Tasks | Status |
|-------|-------------|-------|--------|
| US16 | Trash (Soft Delete) | T180, T192-T195, T208-T210, T218, T220, T224-T227 | ✅ |
| US17 | Archive | T181, T219, T228-T229 | ✅ |
| US18 | Labels | T184-T186, T189, T191, T196-T203, T205, T211-T212, T214, T234-T243, T250-T257 | ✅ |
| US19 | Reminders | T182, T187-T188, T221-T222, T230-T233, T244-T249 | ✅ |

---

## Phase 14: Image Upload with Cloudflare R2 (NEW)

**Purpose**: Enable image attachments on notes using Cloudflare R2 storage
**Added**: 2025-12-03
**Status**: ⏳ IN PROGRESS
**Agent**: backend-expert (API), frontend-expert (UI)

### 14.1 Backend - Dependencies & Config

- [ ] T258 Add boto3, python-multipart, pillow to pyproject.toml
- [ ] T259 Add R2 settings to config.py (R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, R2_PUBLIC_URL)
- [ ] T260 Update .env.example with R2 environment variables

**Checkpoint**: Backend dependencies installed, config ready

### 14.2 Backend - R2 Service

- [ ] T261 [US20] Create services/ directory
- [ ] T262 [US20] Create services/r2.py with R2Service class
- [ ] T263 [US20] Implement upload method (put_object to R2)
- [ ] T264 [US22] Implement delete method (delete_object from R2)
- [ ] T265 [US20] Add error handling for R2 operations

**File**: `backend/src/services/r2.py`

### 14.3 Backend - TaskImage Model

- [ ] T266 [US20] Create TaskImage SQLModel class
- [ ] T267 [US20] Add fields: id, task_id, user_id, filename, storage_key, url, size_bytes, mime_type, width, height, created_at
- [ ] T268 [US20] Add indexes on task_id and user_id
- [ ] T269 Update models/__init__.py exports

**File**: `backend/src/models/task_image.py`

### 14.4 Backend - Image Schemas

- [ ] T270 [US20] Create ImageResponse schema
- [ ] T271 [US20] Add validation for image fields

**File**: `backend/src/schemas/image.py`

### 14.5 Backend - Images Router

- [ ] T272 [US20] Create images router
- [ ] T273 [US20] Implement POST `/tasks/{id}/images` (upload endpoint)
- [ ] T274 [US20] Add file validation (type: JPEG/PNG/GIF/WebP, size: max 5MB)
- [ ] T275 [US20] Add max images per task validation (10)
- [ ] T276 [US20] Extract image dimensions with Pillow
- [ ] T277 [US20] Generate UUID-based storage key
- [ ] T278 [US20] Implement GET `/tasks/{id}/images` (list endpoint)
- [ ] T279 [US22] Implement DELETE `/images/{id}` (delete endpoint)
- [ ] T280 [US22] Delete from R2 when deleting image record
- [ ] T281 Register images router in main.py

**File**: `backend/src/routers/images.py`

**Checkpoint**: Backend API complete - upload, list, delete working

### 14.6 Frontend - Types & API

- [ ] T282 [US20] Add TaskImage type to types/index.ts
- [ ] T283 [US20] Add images field to Task type (optional TaskImage[])
- [ ] T284 [US20] Create imagesApi.upload method (FormData)
- [ ] T285 [US20] Create imagesApi.list method
- [ ] T286 [US22] Create imagesApi.delete method

**Files**: `frontend/src/types/index.ts`, `frontend/src/lib/api.ts`

### 14.7 Frontend - ImageUpload Component

- [ ] T287 [US20] Create ImageUpload component
- [ ] T288 [US20] Add hidden file input with image type filter
- [ ] T289 [US20] Add upload button with Image icon
- [ ] T290 [US20] Client-side file validation (type, size)
- [ ] T291 [US20] Show error toast for invalid files
- [ ] T292 [US20] Show loading state during upload
- [ ] T293 [US20] Call onUpload callback on success

**File**: `frontend/src/components/image-upload.tsx`

### 14.8 Frontend - ImageGallery Component

- [ ] T294 [US20] Create ImageGallery component
- [ ] T295 [US20] Display image thumbnails in grid
- [ ] T296 [US21] Click thumbnail to open viewer
- [ ] T297 [US22] Show delete button on hover
- [ ] T298 [US22] Confirm before delete
- [ ] T299 [US22] Call onDelete callback

**File**: `frontend/src/components/image-gallery.tsx`

### 14.9 Frontend - ImageViewer Component

- [ ] T300 [US21] Create ImageViewer modal component
- [ ] T301 [US21] Full-size image display
- [ ] T302 [US21] Close on Escape or click outside
- [ ] T303 [US21] Navigation arrows for multiple images
- [ ] T304 [US21] Framer Motion animations

**File**: `frontend/src/components/image-viewer.tsx`

### 14.10 Frontend - Integration

- [ ] T305 [US20] Add ImageGallery to task-card.tsx
- [ ] T306 [US20] Add ImageUpload to todo-modal.tsx
- [ ] T307 [US20] Wire up "Add image" button in task-form.tsx
- [ ] T308 [US20] Fetch images when loading task details
- [ ] T309 Refresh task list after image upload/delete

**Files**: `frontend/src/components/task-card.tsx`, `frontend/src/components/todo-modal.tsx`, `frontend/src/components/task-form.tsx`

### 14.11 Testing & Polish

- [ ] T310 Test upload with valid images (JPEG, PNG, GIF, WebP)
- [ ] T311 Test upload rejection for invalid types
- [ ] T312 Test upload rejection for files > 5MB
- [ ] T313 Test max 10 images per task limit
- [ ] T314 Test image deletion
- [ ] T315 Test image viewer navigation
- [ ] T316 Performance check: upload under 5 seconds for 5MB
- [ ] T317 Verify images display correctly in dark/light mode

**Checkpoint**: Image upload feature complete

---

## Phase 14 User Story Summary

| Story | Description | Tasks | Status |
|-------|-------------|-------|--------|
| US20 | Upload Image to Note | T258-T293, T305-T309 | ⏳ |
| US21 | View Image Full Size | T296, T300-T304 | ⏳ |
| US22 | Delete Image from Note | T264, T279-T280, T297-T299 | ⏳ |

---

## Updated Task Summary (Final)

| Phase | Task Count | Completed | Status |
|-------|------------|-----------|--------|
| Phase 1-11: Core App | 103 | 103 | ✅ |
| Phase 12: UI/UX Enhancement | 76 | 76 | ✅ |
| Phase 13: Advanced Features | 78 | 78 | ✅ |
| **Phase 14: Image Upload** | **60** | **0** | **⏳** |
| **Total** | **317** | **257** | **81%** |
