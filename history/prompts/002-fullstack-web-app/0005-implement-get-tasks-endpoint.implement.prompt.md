---
id: 0005
title: Implement GET /api/tasks endpoint
stage: implement
date: 2026-01-22
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-fullstack-web-app
branch: 002-fullstack-web-app
user: venisa-sara
command: backend-expert agent
labels: ["backend", "api", "tasks", "authentication", "testing", "hackathon"]
links:
  spec: /home/dell/evolution-of-todo/specs/002-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/dell/evolution-of-todo/phase-2-web/backend/src/routers/tasks.py
  - /home/dell/evolution-of-todo/phase-2-web/backend/src/routers/__init__.py
  - /home/dell/evolution-of-todo/phase-2-web/backend/src/main.py
  - /home/dell/evolution-of-todo/phase-2-web/backend/tests/test_tasks.py
tests:
  - tests/test_tasks.py::TestListTasks::test_list_tasks_returns_empty_list
  - tests/test_tasks.py::TestListTasks::test_list_tasks_returns_user_tasks
  - tests/test_tasks.py::TestListTasks::test_list_tasks_requires_authentication
  - tests/test_tasks.py::TestListTasks::test_list_tasks_filters_by_user_id
  - tests/test_tasks.py::TestListTasks::test_list_tasks_returns_tasks_in_descending_order
  - tests/test_tasks.py::TestListTasks::test_list_tasks_response_schema
  - tests/test_tasks.py::TestListTasks::test_list_tasks_only_returns_own_tasks
---

## Prompt

You are the backend-expert agent. Complete tasks T047-T050 for User Story 3 (View Task List) - Backend API.

## Context
- Working directory: /home/dell/evolution-of-todo/phase-2-web/backend
- Database is configured in src/database.py
- Task model exists in src/models/task.py
- Pydantic schemas exist in src/schemas/task.py
- Auth dependency exists in src/auth.py (get_current_user)
- FastAPI app exists in src/main.py

## Your Tasks (T047-T050)

- T047: Create tasks router in src/routers/tasks.py
- T048: Implement GET /api/tasks endpoint (list user's tasks)
- T049: Add user_id filtering to ensure users only see their own tasks
- T050: Write pytest tests for GET /api/tasks in tests/test_tasks.py

## Response snapshot

Successfully implemented the GET /api/tasks endpoint with the following components:

1. **Tasks Router** (src/routers/tasks.py):
   - Created FastAPI router with /tasks prefix
   - Implemented list_tasks endpoint that retrieves all tasks for authenticated user
   - Applied get_current_user dependency for authentication
   - Added user_id filtering in SQL query to ensure data isolation
   - Ordered results by created_at descending (newest first)

2. **Router Registration** (src/routers/__init__.py):
   - Exported tasks_router for easy import
   - Followed proper module structure

3. **App Integration** (src/main.py):
   - Imported tasks_router
   - Registered router with /api prefix
   - Router now mounted at /api/tasks

4. **Comprehensive Tests** (tests/test_tasks.py):
   - Created 7 test cases covering:
     - Empty list response
     - Returning user's tasks
     - Authentication requirement (401 when no auth)
     - User ID filtering
     - Descending order by created_at
     - Response schema validation
     - Data isolation (only own tasks)
   - Used pytest fixtures for proper test isolation
   - All tests pass successfully

## Outcome

- ✅ Impact: Implemented first authenticated API endpoint for tasks with proper user isolation
- 🧪 Tests: 7 tests created, all passing (100% success rate)
- 📁 Files: 4 files created/modified (1 new router, 1 updated main, 1 updated __init__, 1 new test file)
- 🔁 Next prompts: Implement POST /api/tasks (Create Task), GET /api/tasks/{id} (Get Task Detail)
- 🧠 Reflection: JWT authentication integration worked smoothly. Test isolation required proper fixture setup to avoid state bleeding between tests.

## Evaluation notes (flywheel)

- Failure modes observed: Initial test failures due to dependency override not being reset between tests. Fixed by implementing pytest fixtures with autouse=True for proper cleanup.
- Graders run and results (PASS/FAIL): PASS - All 7 tests passing
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add pagination support for large task lists (optional enhancement for future)
