# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-01-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

## Summary

Add a conversational AI interface to the existing Todo application using OpenAI ChatKit (frontend), Agents SDK (orchestration), and MCP tools (task operations). Users manage tasks through natural language, with conversation state persisted to database for stateless server architecture.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Node.js 22+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK (backend); Next.js 16, @openai/chatkit (frontend)
**Storage**: Neon Serverless PostgreSQL (existing + new tables)
**Testing**: pytest (backend), vitest (frontend)
**Target Platform**: Web application (browser + server)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Response streaming < 2s, 50 concurrent sessions
**Constraints**: Stateless server (conversation persisted to DB), JWT authentication
**Scale/Scope**: Single user per conversation, 5 MCP tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec complete, plan derived from spec |
| II. Clean Code | ✅ PASS | Will follow PEP 8, type hints, docstrings |
| III. Test-First Development | ✅ PASS | Tests will be written before implementation |
| IV. Single Responsibility | ✅ PASS | Service layer extraction, separated concerns |
| V. Evolutionary Architecture | ✅ PASS | Extends Phase 2 without breaking changes |
| VI. User Experience First | ✅ PASS | Chat UI, streaming responses, helpful errors |

**Gate Result**: PASSED - No violations, ready for Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── chat-api.yaml    # OpenAPI spec for chat endpoint
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (phase-3-chatbot/)

```text
phase-3-chatbot/
├── backend/
│   └── src/
│       ├── models/
│       │   ├── task.py           # Existing
│       │   ├── label.py          # Existing
│       │   ├── conversation.py   # NEW: Conversation model
│       │   └── message.py        # NEW: Message model
│       ├── services/             # NEW: Service layer
│       │   ├── __init__.py
│       │   ├── task_service.py   # Extracted from routers
│       │   └── conversation_service.py
│       ├── agents/               # NEW: Agents SDK
│       │   ├── __init__.py
│       │   ├── factory.py        # Model factory
│       │   └── todo_agent.py     # Main agent
│       ├── mcp/                  # NEW: MCP tools
│       │   ├── __init__.py
│       │   └── tools.py          # 5 MCP tools
│       ├── routers/
│       │   ├── tasks.py          # MODIFY: Use service layer
│       │   └── chat.py           # NEW: Chat endpoint
│       ├── schemas/
│       │   └── chat.py           # NEW: Chat schemas
│       └── main.py               # MODIFY: Register chat router
└── frontend/
    └── src/
        ├── components/
        │   └── chatkit/          # NEW: ChatKit components
        │       ├── ChatKitProvider.tsx
        │       └── ChatKitWidget.tsx
        └── app/
            └── chat/             # NEW: Chat page
                └── page.tsx
```

**Structure Decision**: Web application pattern selected (frontend + backend). Phase 3 builds on Phase 2 structure with additions for AI chatbot functionality.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend (Next.js + ChatKit)                                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ /app/chat/page.tsx → ChatKitWidget                      │ │
│ │ - Custom fetch with Better Auth JWT                     │ │
│ │ - Streaming SSE responses                               │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ POST /api/chat
┌─────────────────────────────────────────────────────────────┐
│ Backend (FastAPI)                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ routers/chat.py                                         │ │
│ │ 1. Validate JWT → get user_id                           │ │
│ │ 2. Load/create conversation (conversation_service)      │ │
│ │ 3. Build message history from DB                        │ │
│ │ 4. Run TodoAgent with MCP tools                         │ │
│ │ 5. Stream response via SSE                              │ │
│ │ 6. Save messages to DB                                  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                              │                              │
│                              ▼                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ agents/todo_agent.py (Agents SDK)                       │ │
│ │ - Instructions for task management                      │ │
│ │ - Model via factory.py (OpenAI/Gemini)                  │ │
│ │ - Tools: add_task, list_tasks, complete_task,           │ │
│ │          delete_task, update_task                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                              │                              │
│                              ▼                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ mcp/tools.py (MCP SDK)                                  │ │
│ │ - add_task(user_id, title, description?)                │ │
│ │ - list_tasks(user_id, status?)                          │ │
│ │ - complete_task(user_id, task_id)                       │ │
│ │ - delete_task(user_id, task_id)                         │ │
│ │ - update_task(user_id, task_id, title?, description?)   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                              │                              │
│                              ▼                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ services/task_service.py                                │ │
│ │ - create_task(), list_tasks(), toggle_complete()        │ │
│ │ - delete_task(), update_task()                          │ │
│ │ (Shared by MCP tools AND REST routers)                  │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Neon PostgreSQL                                             │
│ - tasks (existing)                                          │
│ - labels, task_labels, task_images (existing)               │
│ - conversations (NEW)                                       │
│ - messages (NEW)                                            │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Service Layer Extraction
**Decision**: Extract business logic from routers into service layer
**Rationale**: MCP tools and REST endpoints share same logic; single source of truth
**Impact**: task_service.py created, routers/tasks.py refactored

### 2. Model Factory Pattern
**Decision**: Centralized `create_model()` for AI provider abstraction
**Rationale**: Support OpenAI and Gemini via environment variables
**Impact**: agents/factory.py controls all model instantiation

### 3. In-Process MCP Tools
**Decision**: MCP tools run in same process as FastAPI (not subprocess)
**Rationale**: Lower latency, simpler debugging, shared database session
**Impact**: function_tool pattern, direct service calls

### 4. Stateless Chat Architecture
**Decision**: All conversation state persisted to database
**Rationale**: Hackathon requirement; enables horizontal scaling
**Impact**: conversation_service.py, Conversation/Message models

### 5. SSE Streaming
**Decision**: Stream responses via Server-Sent Events
**Rationale**: Better UX, shows real-time typing, matches ChatKit expectations
**Impact**: StreamingResponse in chat router, Runner.run_streamed()

## Implementation Phases

### Phase A: Service Layer Foundation
1. Create `services/task_service.py` with extracted CRUD logic
2. Create `services/__init__.py`
3. Refactor `routers/tasks.py` to use task_service
4. Verify existing tests still pass

### Phase B: Database Models
5. Create `models/conversation.py`
6. Create `models/message.py`
7. Create `services/conversation_service.py`
8. Add database migration (if needed)

### Phase C: MCP Tools
9. Create `mcp/__init__.py`
10. Create `mcp/tools.py` with 5 tools using task_service

### Phase D: Agent Integration
11. Create `agents/__init__.py`
12. Create `agents/factory.py` (model factory)
13. Create `agents/todo_agent.py` (TodoAgent with MCP tools)

### Phase E: Chat API
14. Create `schemas/chat.py` (request/response schemas)
15. Create `routers/chat.py` (POST /api/chat with SSE streaming)
16. Register chat router in `main.py`

### Phase F: Frontend ChatKit
17. Create `components/chatkit/ChatKitWidget.tsx`
18. Create `components/chatkit/ChatKitProvider.tsx`
19. Create `app/chat/page.tsx`
20. Add environment variables

### Phase G: Testing & Polish
21. Backend integration tests for chat endpoint
22. E2E test for conversation flow
23. Error handling improvements
24. Documentation updates

## Environment Variables (New)

### Backend
```env
# AI Provider
LLM_PROVIDER=openai          # or "gemini"
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini
# Optional Gemini
GEMINI_API_KEY=...
GEMINI_DEFAULT_MODEL=gemini-2.0-flash
```

### Frontend
```env
NEXT_PUBLIC_CHATKIT_API_URL=/api/chat
```

## Dependencies (New)

### Backend (pyproject.toml)
```toml
[project.dependencies]
openai-agents = ">=0.1.0"
mcp = ">=1.0.0"
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "@openai/chatkit": "^0.1.0"
  }
}
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| ChatKit SDK unavailable/unstable | Fallback to custom chat UI component |
| Streaming complexity | Start with non-streaming, add streaming later |
| MCP SDK learning curve | Reference chatkit-backend-engineer agent examples |
| Model rate limits | Implement retry with exponential backoff |

## Complexity Tracking

> No violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
