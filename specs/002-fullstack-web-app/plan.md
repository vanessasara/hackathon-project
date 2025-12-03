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

---

## Phase 2.1: UI/UX Enhancement - Google Keep Style

**Added**: 2025-12-03
**Goal**: Transform the basic todo interface into a polished Google Keep-inspired UI

### Design Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Theme System | next-themes + CSS Variables | SSR-safe, Tailwind-compatible, localStorage persistence |
| Animation Library | Framer Motion | React-native animations, layout animations, exit animations |
| Grid Layout | CSS Columns (masonry) | Native CSS, no JS calculation, responsive |
| Color System | 12-color palette | Google Keep standard, tested for accessibility |

### Theme Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       THEME SYSTEM                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CSS Variables define colors                                  │
│     :root { --background: #ffffff; --foreground: #202124; ... }  │
│     .dark { --background: #202124; --foreground: #e8eaed; ... }  │
│                                                                  │
│  2. next-themes manages dark class on <html>                     │
│     <ThemeProvider attribute="class" defaultTheme="system">      │
│                                                                  │
│  3. Tailwind uses CSS variables                                  │
│     bg-background → var(--background)                            │
│     text-foreground → var(--foreground)                          │
│                                                                  │
│  4. Components auto-adapt to theme                               │
│     No conditional className logic needed                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Color Palette

```typescript
// 12 Google Keep colors with light/dark variants
const KEEP_COLORS = {
  default: { light: '#ffffff', dark: '#28292c' },
  coral:   { light: '#f28b82', dark: '#77172e' },
  peach:   { light: '#fbbc04', dark: '#692b17' },
  sand:    { light: '#fff475', dark: '#7c4a03' },
  mint:    { light: '#ccff90', dark: '#264d3b' },
  sage:    { light: '#a7ffeb', dark: '#0c625d' },
  fog:     { light: '#cbf0f8', dark: '#256377' },
  storm:   { light: '#aecbfa', dark: '#1e3a5f' },
  dusk:    { light: '#d7aefb', dark: '#42275e' },
  blossom: { light: '#fdcfe8', dark: '#5b2245' },
  clay:    { light: '#e6c9a8', dark: '#442f19' },
  chalk:   { light: '#e8eaed', dark: '#3c3f43' },
};
```

### Layout Structure

```
┌──────────────────────────────────────────────────────────────┐
│ ☰  │  🔍 Search Keep...                    ⊞ 🌙 ⚙️ 👤       │ Header
├────┼─────────────────────────────────────────────────────────┤
│ 💡 │                                                         │
│ 🔔 │  ┌─────────────────────────────────────────────────┐   │ Expandable
│ ✏️ │  │ Take a note...                    ☑️ 🖌️ 🖼️       │   │ Input
│ 📦 │  └─────────────────────────────────────────────────┘   │
│ 🗑️ │                                                         │ Sidebar
│    │  📌 PINNED                                             │
│    │  ┌─────┐ ┌─────┐ ┌─────┐                              │
│    │  │Card │ │Card │ │Card │                              │ Masonry
│    │  └─────┘ └─────┘ └─────┘                              │ Grid
│    │                                                         │
│    │  🏷️ OTHERS                                             │
│    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                      │
│    │  │Card │ │     │ │Card │ │     │                      │
│    │  └─────┘ │Card │ └─────┘ │Card │                      │
│    │          └─────┘         └─────┘                      │
└────┴─────────────────────────────────────────────────────────┘
```

### New Components

```text
phase-2-web/frontend/src/
├── components/
│   ├── theme-toggle.tsx        # Dark/light mode switch
│   ├── sidebar.tsx             # Left navigation
│   ├── view-toggle.tsx         # Grid/List switch
│   ├── color-picker.tsx        # 12-color selector
│   ├── todo-modal.tsx          # Edit modal with backdrop
│   ├── expandable-input.tsx    # "Take a note..." input
│   └── masonry-grid.tsx        # CSS columns grid
└── lib/
    └── theme-provider.tsx      # next-themes wrapper
```

### Database Schema Updates

```python
# Task model additions (backend/src/models/task.py)
class Task(SQLModel, table=True):
    # ... existing fields
    color: str = Field(default="default")  # One of 12 color keys
    pinned: bool = Field(default=False)    # Pin to top of list
```

### API Updates

| Method | Endpoint | Changes |
|--------|----------|---------|
| POST | `/api/tasks` | Accept `color`, `pinned` in body |
| PATCH | `/api/tasks/{id}` | Accept `color`, `pinned` updates |
| GET | `/api/tasks` | Return `color`, `pinned` fields; sort pinned first |

### Animation Specifications

| Component | Animation | Duration | Easing |
|-----------|-----------|----------|--------|
| Card enter | scale 0.8→1, opacity 0→1 | 300ms | spring(300, 24) |
| Card exit | scale 1→0.9, opacity 1→0 | 200ms | ease-out |
| Card hover | scale 1→1.02, shadow lift | 200ms | spring(400, 17) |
| Modal open | scale 0.95→1, opacity 0→1 | 300ms | spring(300, 25) |
| Modal close | scale 1→0.95, opacity 1→0 | 200ms | ease-in |
| Sidebar | width 0→280px | 300ms | ease-in-out |
| Theme toggle | rotate 180° | 500ms | spring(200, 10) |

### Agent Assignments (Phase 2.1)

| Component | Agent |
|-----------|-------|
| Theme system | frontend-expert |
| Sidebar | frontend-expert |
| Masonry grid | frontend-expert |
| Card redesign | frontend-expert |
| Color picker | frontend-expert |
| Todo modal | frontend-expert |
| Animations | frontend-expert |
| Backend updates | backend-expert |

---

## Phase 2.2: Advanced Features - Trash, Archive, Labels & Reminders

**Added**: 2025-12-03
**Status**: Completed
**Goal**: Add Google Keep-inspired organization features

### Database Schema Updates

#### Task Model Additions
```python
# backend/src/models/task.py - New fields
class Task(SQLModel, table=True):
    # ... existing fields (id, user_id, title, description, completed, pinned, color)
    deleted_at: Optional[datetime] = Field(default=None)  # Soft delete timestamp
    archived: bool = Field(default=False, index=True)     # Archive flag
    reminder_at: Optional[datetime] = Field(default=None, index=True)  # Reminder datetime
```

#### New Label Model
```python
# backend/src/models/label.py
class Label(SQLModel, table=True):
    __tablename__ = "labels"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    name: str = Field(max_length=50)
    created_at: datetime
    updated_at: datetime
```

#### New TaskLabel Junction Table
```python
# backend/src/models/task_label.py
class TaskLabel(SQLModel, table=True):
    __tablename__ = "task_labels"
    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    label_id: int = Field(foreign_key="labels.id", primary_key=True)
```

### API Endpoints (Phase 2.2)

#### Tasks Router Updates

| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/api/tasks` | List tasks | `filter` (active/trash/archive/reminders), `label_id` |
| DELETE | `/api/tasks/{id}` | Soft delete (sets deleted_at) | - |
| POST | `/api/tasks/{id}/restore` | Restore from trash | - |
| DELETE | `/api/tasks/{id}/permanent` | Permanent delete | - |
| DELETE | `/api/tasks/trash/empty` | Empty all trash | - |
| POST | `/api/tasks/{id}/labels/{label_id}` | Add label to task | - |
| DELETE | `/api/tasks/{id}/labels/{label_id}` | Remove label from task | - |

#### New Labels Router

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/labels` | List user's labels |
| POST | `/api/labels` | Create label |
| GET | `/api/labels/{id}` | Get single label |
| PATCH | `/api/labels/{id}` | Update label name |
| DELETE | `/api/labels/{id}` | Delete label |

### Frontend Routes (Phase 2.2)

```
/dashboard              → Main notes (filter=active, excludes deleted/archived)
/dashboard/trash        → Trashed notes (filter=trash)
/dashboard/archive      → Archived notes (filter=archive)
/dashboard/reminders    → Notes with reminders (filter=reminders, grouped by SENT/UPCOMING)
/dashboard/labels/[id]  → Filter by specific label
```

### New Components (Phase 2.2)

```text
phase-2-web/frontend/src/
├── app/dashboard/
│   ├── trash/page.tsx           # Trash view with Empty Trash button, 7-day warning
│   ├── archive/page.tsx         # Archive view
│   ├── reminders/page.tsx       # Reminders with SENT/UPCOMING sections
│   └── labels/[labelId]/page.tsx # Dynamic label filter route
├── components/
│   ├── edit-labels-modal.tsx    # Label CRUD modal
│   └── reminder-picker.tsx      # Google Keep style reminder picker
```

### Design Decisions (Phase 2.2)

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Soft Delete | `deleted_at` timestamp | Allows tracking deletion time, null = active |
| 7-Day Warning | Display only | No background jobs/cron - just UI message |
| Reminder Picker | Google Keep presets | Today 8PM, Tomorrow 8AM, Next week Monday 8AM + custom |
| Labels | Many-to-many junction | Tasks can have multiple labels |
| Context-Aware Cards | Different actions per route | Trash shows restore/delete forever, Archive shows unarchive |

### Reminder Picker Presets

```typescript
const presets = [
  { label: "Today 8:00 PM", date: today8PM, enabled: now < today8PM },
  { label: "Tomorrow 8:00 AM", date: tomorrow8AM, enabled: true },
  { label: "Next week Monday 8:00 AM", date: nextMonday8AM, enabled: true },
];
// Plus "Pick date & time" option for custom datetime
```

### Context-Aware TaskCard Actions

| Route | Available Actions |
|-------|-------------------|
| `/dashboard` (normal) | Reminder, Color, Archive, Delete, Pin |
| `/dashboard/trash` | Restore, Delete forever |
| `/dashboard/archive` | Unarchive, Delete |

### Agent Assignments (Phase 2.2)

| Component | Agent |
|-----------|-------|
| Task model updates | backend-expert |
| Label model + router | backend-expert |
| Tasks router filter updates | backend-expert |
| Trash/Archive/Reminders pages | frontend-expert |
| Label filter page | frontend-expert |
| EditLabelsModal | frontend-expert |
| ReminderPicker | frontend-expert |
| TaskCard context actions | frontend-expert |
| Sidebar dynamic labels | frontend-expert |

---

## Phase 2.3: Image Upload with Cloudflare R2

**Added**: 2025-12-03
**Status**: In Progress
**Goal**: Enable image attachments on notes using Cloudflare R2 storage

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           IMAGE UPLOAD FLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. User selects image file                                              │
│     ┌─────────┐         ┌─────────────────┐                             │
│     │ Browser │ ──────► │ File Input      │                             │
│     └─────────┘         │ (5MB max)       │                             │
│                         └────────┬────────┘                             │
│                                  │                                       │
│  2. Frontend sends to Backend (multipart/form-data)                      │
│     ┌─────────┐         ┌─────────────────┐         ┌──────────────┐   │
│     │ Browser │ ──────► │ POST /tasks/    │ ──────► │ FastAPI      │   │
│     │         │   JWT   │ {id}/images     │         │ Validates    │   │
│     └─────────┘         └─────────────────┘         └──────┬───────┘   │
│                                                            │            │
│  3. Backend uploads to Cloudflare R2                       │            │
│     ┌──────────────┐    ┌─────────────────┐         ┌──────▼───────┐   │
│     │ R2 Bucket    │ ◄── │ boto3 S3 client │ ◄────── │ R2 Service   │   │
│     │ (storage)    │    │ (put_object)    │         │ (upload)     │   │
│     └──────────────┘    └─────────────────┘         └──────────────┘   │
│                                                                          │
│  4. Database stores metadata, returns public URL                         │
│     ┌─────────┐         ┌─────────────────┐         ┌──────────────┐   │
│     │ Browser │ ◄────── │ TaskImage       │ ◄────── │ PostgreSQL   │   │
│     │ (URL)   │         │ Response        │         │ (metadata)   │   │
│     └─────────┘         └─────────────────┘         └──────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Database Schema

```python
# backend/src/models/task_image.py
class TaskImage(SQLModel, table=True):
    __tablename__ = "task_images"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id", index=True)
    user_id: str = Field(index=True)  # Denormalized for fast queries

    filename: str = Field(max_length=255)      # Original filename
    storage_key: str = Field(max_length=500)   # R2 object key
    url: str = Field(max_length=1000)          # Public URL

    size_bytes: int = Field(default=0)
    mime_type: str = Field(max_length=100, default="image/jpeg")
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)

    created_at: datetime = Field(default_factory=_utc_now)
```

**Storage Key Format:** `{user_id}/{task_id}/{uuid}.{ext}`

### API Endpoints (Phase 2.3)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks/{id}/images` | Upload image (multipart/form-data) |
| GET | `/api/tasks/{id}/images` | List images for task |
| DELETE | `/api/images/{id}` | Delete image from task and R2 |

### Dependencies (New)

**Backend (pyproject.toml)**:
```toml
boto3>=1.35.0           # S3-compatible client for R2
python-multipart>=0.0.9 # File upload parsing
pillow>=11.0.0          # Image validation & dimensions
```

### Environment Variables

```env
# R2 Configuration
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=todo-images
R2_PUBLIC_URL=https://pub-xxx.r2.dev
```

### New Components (Frontend)

```text
phase-2-web/frontend/src/
├── components/
│   ├── image-upload.tsx      # Upload button with drag-drop
│   ├── image-gallery.tsx     # Thumbnail grid display
│   └── image-viewer.tsx      # Full-size modal viewer
```

### File Changes

#### Backend (New)
| File | Description |
|------|-------------|
| `src/models/task_image.py` | TaskImage SQLModel |
| `src/schemas/image.py` | Image schemas |
| `src/services/r2.py` | R2 storage service |
| `src/routers/images.py` | Image upload/delete endpoints |

#### Backend (Modify)
| File | Change |
|------|--------|
| `src/models/__init__.py` | Export TaskImage |
| `src/main.py` | Register images router |
| `src/config.py` | Add R2 settings |
| `pyproject.toml` | Add boto3, python-multipart, pillow |

#### Frontend (New)
| File | Description |
|------|-------------|
| `src/components/image-upload.tsx` | Upload button/dropzone |
| `src/components/image-gallery.tsx` | Thumbnail display |
| `src/components/image-viewer.tsx` | Full-size modal |

#### Frontend (Modify)
| File | Change |
|------|--------|
| `src/types/index.ts` | Add TaskImage type |
| `src/lib/api.ts` | Add imagesApi methods |
| `src/components/task-card.tsx` | Display image thumbnails |
| `src/components/todo-modal.tsx` | Add image upload/manage |
| `src/components/task-form.tsx` | Wire up "Add image" button |

### Design Decisions (Phase 2.3)

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Storage | Cloudflare R2 | S3-compatible, free egress, cost-effective |
| Upload Flow | Backend-mediated | Security (validates ownership), consistent naming |
| Denormalized user_id | Yes | Faster queries without joins |
| UUID filenames | Yes | Prevent collisions and URL guessing |
| Max file size | 5MB | Reasonable for note attachments |
| Max images per task | 10 | Prevents abuse |

### Agent Assignments (Phase 2.3)

| Component | Agent |
|-----------|-------|
| R2 service | backend-expert |
| TaskImage model | backend-expert |
| Images router | backend-expert |
| ImageUpload component | frontend-expert |
| ImageGallery component | frontend-expert |
| ImageViewer component | frontend-expert |
| TaskCard integration | frontend-expert |
