# Implementation Tasks: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Branch**: `003-ai-chatbot`
**Generated**: 2025-12-03
**Total Tasks**: 42

## User Story Mapping

| Story | Priority | Description | Tasks |
|-------|----------|-------------|-------|
| US1 | P1 | Add Task via Natural Language | T017-T019 |
| US2 | P1 | List Tasks via Natural Language | T020-T022 |
| US3 | P1 | Complete Task via Natural Language | T023-T025 |
| US4 | P2 | Delete Task via Natural Language | T026-T028 |
| US5 | P2 | Update Task via Natural Language | T029-T031 |
| US6 | P2 | Conversation Context | T032-T034 |

## Dependency Graph

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ─────────────────────────────┐
    │                                                │
    ├─────────┬─────────┬─────────┐                  │
    ▼         ▼         ▼         ▼                  │
Phase 3    Phase 4    Phase 5    (can run           │
(US1)      (US2)      (US3)      in parallel)       │
    │         │         │                            │
    └─────────┴─────────┴────────────────────────────┤
                                                     │
    ┌─────────┬─────────┬─────────┐                  │
    ▼         ▼         ▼         ▼                  │
Phase 6    Phase 7    Phase 8    (can run           │
(US4)      (US5)      (US6)      in parallel)       │
    │         │         │                            │
    └─────────┴─────────┴────────────────────────────┤
                                                     │
                                                     ▼
                                              Phase 9 (Polish)
```

## MVP Scope

**Suggested MVP**: Complete through Phase 5 (US1, US2, US3)
- Users can add, list, and complete tasks via chat
- Core value proposition delivered
- Can demo end-to-end flow

---

## Phase 1: Setup

**Goal**: Initialize project dependencies and configuration

- [X] T001 Add openai-agents and mcp dependencies to `phase-3-chatbot/backend/pyproject.toml`
- [X] T002 [P] Add AI provider environment variables to `phase-3-chatbot/backend/.env.example`
- [X] T003 [P] Add NEXT_PUBLIC_CHATKIT_API_URL to `phase-3-chatbot/frontend/.env.example`
- [X] T004 Create `phase-3-chatbot/backend/src/services/__init__.py`
- [X] T005 [P] Create `phase-3-chatbot/backend/src/agents/__init__.py`
- [X] T006 [P] Create `phase-3-chatbot/backend/src/mcp/__init__.py`

---

## Phase 2: Foundational

**Goal**: Create shared infrastructure required by all user stories

### Service Layer Extraction

- [X] T007 Create task_service.py with create_task() in `phase-3-chatbot/backend/src/services/task_service.py`
- [X] T008 Add list_tasks() to task_service.py with filter support in `phase-3-chatbot/backend/src/services/task_service.py`
- [X] T009 Add toggle_complete() to task_service.py in `phase-3-chatbot/backend/src/services/task_service.py`
- [X] T010 Add delete_task() and update_task() to task_service.py in `phase-3-chatbot/backend/src/services/task_service.py`
- [X] T011 Refactor routers/tasks.py to use task_service in `phase-3-chatbot/backend/src/routers/tasks.py`

### Database Models

- [X] T012 Create Conversation model in `phase-3-chatbot/backend/src/models/conversation.py`
- [X] T013 Create Message model in `phase-3-chatbot/backend/src/models/message.py`
- [X] T014 Create conversation_service.py with CRUD operations in `phase-3-chatbot/backend/src/services/conversation_service.py`

### Agent Infrastructure

- [X] T015 Create model factory with OpenAI/Gemini support in `phase-3-chatbot/backend/src/agents/factory.py`
- [X] T016 Create chat schemas (ChatRequest, ChatResponse) in `phase-3-chatbot/backend/src/schemas/chat.py`

---

## Phase 3: User Story 1 - Add Task via Natural Language (P1)

**Goal**: Users can add tasks by typing natural language commands
**Independent Test**: Type "Add a task to buy groceries" and verify task created

### MCP Tool

- [X] T017 [US1] Create add_task MCP tool using task_service in `phase-3-chatbot/backend/src/mcp/tools.py`

### Agent Integration

- [X] T018 [US1] Create TodoAgent with add_task tool and instructions in `phase-3-chatbot/backend/src/agents/todo_agent.py`

### Chat Endpoint

- [X] T019 [US1] Create POST /api/chat endpoint with SSE streaming in `phase-3-chatbot/backend/src/routers/chat.py`

---

## Phase 4: User Story 2 - List Tasks via Natural Language (P1)

**Goal**: Users can view tasks by asking the chatbot
**Independent Test**: Type "Show me all my tasks" and verify list returned

### MCP Tool

- [X] T020 [US2] Add list_tasks MCP tool with status filter in `phase-3-chatbot/backend/src/mcp/tools.py`

### Agent Update

- [X] T021 [US2] Add list_tasks tool to TodoAgent in `phase-3-chatbot/backend/src/agents/todo_agent.py`

### Instructions Update

- [X] T022 [US2] Update TodoAgent instructions for list commands in `phase-3-chatbot/backend/src/agents/todo_agent.py`

---

## Phase 5: User Story 3 - Complete Task via Natural Language (P1)

**Goal**: Users can mark tasks complete via chat
**Independent Test**: Type "Mark task 1 as complete" and verify status changes

### MCP Tool

- [X] T023 [US3] Add complete_task MCP tool in `phase-3-chatbot/backend/src/mcp/tools.py`

### Agent Update

- [X] T024 [US3] Add complete_task tool to TodoAgent in `phase-3-chatbot/backend/src/agents/todo_agent.py`

### Instructions Update

- [X] T025 [US3] Update TodoAgent instructions for complete commands in `phase-3-chatbot/backend/src/agents/todo_agent.py`

---

## Phase 6: User Story 4 - Delete Task via Natural Language (P2)

**Goal**: Users can delete tasks via chat
**Independent Test**: Type "Delete task 2" and verify task removed

### MCP Tool

- [X] T026 [US4] Add delete_task MCP tool in `phase-3-chatbot/backend/src/mcp/tools.py`

### Agent Update

- [X] T027 [US4] Add delete_task tool to TodoAgent in `phase-3-chatbot/backend/src/agents/todo_agent.py`

### Instructions Update

- [X] T028 [US4] Update TodoAgent instructions for delete commands in `phase-3-chatbot/backend/src/agents/todo_agent.py`

---

## Phase 7: User Story 5 - Update Task via Natural Language (P2)

**Goal**: Users can update task details via chat
**Independent Test**: Type "Change task 1 to 'Call mom tonight'" and verify update

### MCP Tool

- [X] T029 [US5] Add update_task MCP tool in `phase-3-chatbot/backend/src/mcp/tools.py`

### Agent Update

- [X] T030 [US5] Add update_task tool to TodoAgent in `phase-3-chatbot/backend/src/agents/todo_agent.py`

### Instructions Update

- [X] T031 [US5] Update TodoAgent instructions for update commands in `phase-3-chatbot/backend/src/agents/todo_agent.py`

---

## Phase 8: User Story 6 - Conversation Context (P2)

**Goal**: Chatbot maintains conversation context across messages
**Independent Test**: Ask "Show pending tasks" then "Mark the first one done"

### Conversation Persistence

- [X] T032 [US6] Add conversation history loading to chat endpoint in `phase-3-chatbot/backend/src/routers/chat.py`

### Message History

- [X] T033 [US6] Build message array from DB for agent context in `phase-3-chatbot/backend/src/routers/chat.py`

### Context Instructions

- [X] T034 [US6] Update TodoAgent instructions for multi-turn context in `phase-3-chatbot/backend/src/agents/todo_agent.py`

---

## Phase 9: Frontend ChatKit Integration

**Goal**: Chat UI in frontend

- [ ] T035 Create ChatKitWidget component in `phase-3-chatbot/frontend/src/components/chatkit/ChatKitWidget.tsx`
- [ ] T036 [P] Create ChatKitProvider with auth integration in `phase-3-chatbot/frontend/src/components/chatkit/ChatKitProvider.tsx`
- [ ] T037 Create chat page with ChatKit in `phase-3-chatbot/frontend/src/app/chat/page.tsx`
- [ ] T038 Add navigation link to chat page in `phase-3-chatbot/frontend/src/components/layout/Sidebar.tsx`

---

## Phase 10: Polish & Integration

**Goal**: Final integration, error handling, and documentation

- [X] T039 Register chat router in main.py in `phase-3-chatbot/backend/src/main.py`
- [X] T040 Add error handling for AI model unavailability in `phase-3-chatbot/backend/src/routers/chat.py`
- [X] T041 Add conversation list endpoint (GET /api/conversations) in `phase-3-chatbot/backend/src/routers/chat.py`
- [X] T042 Update phase-3-chatbot README with chat feature documentation in `phase-3-chatbot/README.md`

---

## Parallel Execution Opportunities

### Setup Phase (T001-T006)
```
T001 (deps) → T004, T005, T006 (can start after T001)
T002, T003 can run in parallel with T001
```

### Foundational Phase (T007-T016)
```
T007 → T008 → T009 → T010 → T011 (sequential - service layer)
T012, T013 can run in parallel with service layer
T014 depends on T012, T013
T015, T016 can run in parallel with above
```

### User Story Phases (P1 stories)
```
After Phase 2 complete:
  Phase 3 (US1), Phase 4 (US2), Phase 5 (US3) can run in parallel
  Each phase's tasks are sequential within the phase
```

### User Story Phases (P2 stories)
```
After any P1 story complete:
  Phase 6 (US4), Phase 7 (US5), Phase 8 (US6) can run in parallel
```

### Frontend Phase
```
T035, T036 can run in parallel
T037 depends on T035, T036
T038 can run after T037
```

---

## Implementation Strategy

### MVP First Approach
1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. Complete Phase 3 (US1: Add Task) - **First demo milestone**
4. Complete Phase 4 (US2: List Tasks)
5. Complete Phase 5 (US3: Complete Task) - **MVP complete**

### Incremental Delivery
- After Phase 3: Demo "Add a task to buy groceries"
- After Phase 5: Demo full add/list/complete workflow
- After Phase 8: Demo multi-turn conversations
- After Phase 10: Production-ready feature

### Test Verification Points
- After T011: Existing task tests should pass
- After T019: Can add task via curl
- After T022: Can list tasks via curl
- After T037: Full UI flow works

---

## Task Count Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| Phase 1 (Setup) | 6 | 4 |
| Phase 2 (Foundational) | 10 | 4 |
| Phase 3 (US1) | 3 | 0 |
| Phase 4 (US2) | 3 | 0 |
| Phase 5 (US3) | 3 | 0 |
| Phase 6 (US4) | 3 | 0 |
| Phase 7 (US5) | 3 | 0 |
| Phase 8 (US6) | 3 | 0 |
| Phase 9 (Frontend) | 4 | 2 |
| Phase 10 (Polish) | 4 | 0 |
| **Total** | **42** | **10** |
