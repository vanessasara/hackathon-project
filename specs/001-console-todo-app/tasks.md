# Tasks: Console Todo App

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: REQUIRED per Constitution Principle III (Test-First Development is NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project root**: `phase-1-console/`
- **Source**: `phase-1-console/src/todo/`
- **Tests**: `phase-1-console/tests/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure

- [x] T001 Create phase-1-console directory structure per implementation plan
- [x] T002 Initialize UV project with pyproject.toml in phase-1-console/
- [x] T003 Add pytest as dev dependency via `uv add --dev pytest`
- [x] T004 [P] Create package structure: phase-1-console/src/todo/__init__.py
- [x] T005 [P] Create test package: phase-1-console/tests/__init__.py

---

## Phase 2: Foundational (Task Model & Manager Core)

**Purpose**: Core data model and manager that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational (Red Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T006 [P] Create test file for Task model in phase-1-console/tests/test_models.py
- [x] T007 [P] Create test file for TaskManager in phase-1-console/tests/test_manager.py
- [x] T008 Write test_task_creation_with_required_fields in tests/test_models.py
- [x] T009 Write test_task_default_values in tests/test_models.py (completed=False, created_at auto-set)
- [x] T010 Write test_task_manager_initialization in tests/test_manager.py

### Implementation for Foundational (Green Phase)

- [x] T011 Implement Task dataclass in phase-1-console/src/todo/models.py per data-model.md
- [x] T012 Implement TaskManager.__init__ with empty list and ID counter in phase-1-console/src/todo/manager.py
- [x] T013 Verify tests pass (Green): `uv run pytest tests/test_models.py tests/test_manager.py`

**Checkpoint**: Foundation ready - Task model and TaskManager skeleton exist and pass tests

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all their tasks displayed in a list with ID, title, status, and creation date

**Independent Test**: Launch app, select "View all tasks" from menu, verify output format

### Tests for User Story 1 (Red Phase)

- [x] T014 [P] [US1] Write test_get_all_tasks_empty in tests/test_manager.py
- [x] T015 [P] [US1] Write test_get_all_tasks_returns_list in tests/test_manager.py
- [x] T016 [P] [US1] Write test_has_tasks_false_when_empty in tests/test_manager.py
- [x] T017 [P] [US1] Write test_has_tasks_true_with_tasks in tests/test_manager.py
- [x] T018 [P] [US1] Create UI test file phase-1-console/tests/test_ui.py
- [x] T019 [US1] Write test_format_task_list_empty in tests/test_ui.py
- [x] T020 [US1] Write test_format_task_list_with_tasks in tests/test_ui.py

### Implementation for User Story 1 (Green Phase)

- [x] T021 [US1] Implement TaskManager.get_all_tasks() in phase-1-console/src/todo/manager.py
- [x] T022 [US1] Implement TaskManager.has_tasks() in phase-1-console/src/todo/manager.py
- [x] T023 [US1] Implement TaskManager.task_count() in phase-1-console/src/todo/manager.py
- [x] T024 [US1] Implement format_task_list() in phase-1-console/src/todo/ui.py
- [x] T025 [US1] Implement format_empty_list_message() in phase-1-console/src/todo/ui.py
- [x] T026 [US1] Verify tests pass (Green): `uv run pytest -k US1 or test_get_all or test_has_tasks or test_format_task`

**Checkpoint**: User Story 1 complete - can view task list (empty message or formatted list)

---

## Phase 4: User Story 2 - Add New Task (Priority: P2)

**Goal**: Users can create new tasks with title (required) and description (optional)

**Independent Test**: Select "Add new task", enter title/description, verify task appears in list

### Tests for User Story 2 (Red Phase)

- [x] T027 [P] [US2] Write test_add_task_returns_task_with_id in tests/test_manager.py
- [x] T028 [P] [US2] Write test_add_task_sequential_ids in tests/test_manager.py
- [x] T029 [P] [US2] Write test_add_task_with_description in tests/test_manager.py
- [x] T030 [P] [US2] Write test_add_task_empty_title_raises_error in tests/test_manager.py
- [x] T031 [P] [US2] Write test_add_task_title_too_long_raises_error in tests/test_manager.py
- [x] T032 [P] [US2] Write test_add_task_description_too_long_raises_error in tests/test_manager.py
- [x] T033 [US2] Write test_validate_title_input in tests/test_ui.py
- [x] T034 [US2] Write test_prompt_for_title in tests/test_ui.py

### Implementation for User Story 2 (Green Phase)

- [x] T035 [US2] Implement title validation (1-200 chars) in phase-1-console/src/todo/manager.py
- [x] T036 [US2] Implement description validation (max 1000 chars) in phase-1-console/src/todo/manager.py
- [x] T037 [US2] Implement TaskManager.add_task() in phase-1-console/src/todo/manager.py
- [x] T038 [US2] Implement prompt_for_title() in phase-1-console/src/todo/ui.py
- [x] T039 [US2] Implement prompt_for_description() in phase-1-console/src/todo/ui.py
- [x] T040 [US2] Implement display_task_created_message() in phase-1-console/src/todo/ui.py
- [x] T041 [US2] Verify tests pass (Green): `uv run pytest -k "add_task or validate_title or prompt"`

**Checkpoint**: User Stories 1 AND 2 complete - can add tasks and view them

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P3)

**Goal**: Users can toggle task completion status by ID

**Independent Test**: Add task, select "Mark complete", enter ID, verify status changes in view

### Tests for User Story 3 (Red Phase)

- [x] T042 [P] [US3] Write test_toggle_complete_pending_to_completed in tests/test_manager.py
- [x] T043 [P] [US3] Write test_toggle_complete_completed_to_pending in tests/test_manager.py
- [x] T044 [P] [US3] Write test_toggle_complete_not_found_raises_error in tests/test_manager.py
- [x] T045 [US3] Write test_prompt_for_task_id in tests/test_ui.py
- [x] T046 [US3] Write test_display_toggle_success_message in tests/test_ui.py

### Implementation for User Story 3 (Green Phase)

- [x] T047 [US3] Implement TaskManager.get_task() in phase-1-console/src/todo/manager.py
- [x] T048 [US3] Implement TaskManager.toggle_complete() in phase-1-console/src/todo/manager.py
- [x] T049 [US3] Implement prompt_for_task_id() in phase-1-console/src/todo/ui.py
- [x] T050 [US3] Implement display_toggle_message() in phase-1-console/src/todo/ui.py
- [x] T051 [US3] Verify tests pass (Green): `uv run pytest -k "toggle_complete or task_id"`

**Checkpoint**: User Stories 1, 2, AND 3 complete - can add tasks, view them, toggle completion

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Users can modify task title and/or description

**Independent Test**: Add task, select "Update", enter ID and new values, verify changes in view

### Tests for User Story 4 (Red Phase)

- [x] T052 [P] [US4] Write test_update_task_title in tests/test_manager.py
- [x] T053 [P] [US4] Write test_update_task_description in tests/test_manager.py
- [x] T054 [P] [US4] Write test_update_task_both_fields in tests/test_manager.py
- [x] T055 [P] [US4] Write test_update_task_keep_original_if_none in tests/test_manager.py
- [x] T056 [P] [US4] Write test_update_task_not_found_raises_error in tests/test_manager.py
- [x] T057 [US4] Write test_prompt_for_new_title in tests/test_ui.py
- [x] T058 [US4] Write test_prompt_for_new_description in tests/test_ui.py

### Implementation for User Story 4 (Green Phase)

- [x] T059 [US4] Implement TaskManager.update_task() in phase-1-console/src/todo/manager.py
- [x] T060 [US4] Implement prompt_for_new_title() (with skip option) in phase-1-console/src/todo/ui.py
- [x] T061 [US4] Implement prompt_for_new_description() (with skip option) in phase-1-console/src/todo/ui.py
- [x] T062 [US4] Implement display_update_success_message() in phase-1-console/src/todo/ui.py
- [x] T063 [US4] Verify tests pass (Green): `uv run pytest -k "update_task or new_title or new_description"`

**Checkpoint**: User Stories 1-4 complete - full CRUD except delete

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Users can remove tasks with confirmation prompt

**Independent Test**: Add task, select "Delete", enter ID, confirm, verify task removed from list

### Tests for User Story 5 (Red Phase)

- [x] T064 [P] [US5] Write test_delete_task_removes_from_list in tests/test_manager.py
- [x] T065 [P] [US5] Write test_delete_task_returns_deleted_task in tests/test_manager.py
- [x] T066 [P] [US5] Write test_delete_task_not_found_raises_error in tests/test_manager.py
- [x] T067 [US5] Write test_prompt_delete_confirmation in tests/test_ui.py
- [x] T068 [US5] Write test_display_delete_success_message in tests/test_ui.py

### Implementation for User Story 5 (Green Phase)

- [x] T069 [US5] Implement TaskManager.delete_task() in phase-1-console/src/todo/manager.py
- [x] T070 [US5] Implement prompt_delete_confirmation() in phase-1-console/src/todo/ui.py
- [x] T071 [US5] Implement display_delete_success_message() in phase-1-console/src/todo/ui.py
- [x] T072 [US5] Implement display_delete_cancelled_message() in phase-1-console/src/todo/ui.py
- [x] T073 [US5] Verify tests pass (Green): `uv run pytest -k "delete_task or delete_confirmation"`

**Checkpoint**: User Stories 1-5 complete - full CRUD operations working

---

## Phase 8: User Story 6 - Navigate Menu and Exit (Priority: P6)

**Goal**: Clear menu interface with all options and clean exit with data warning

**Independent Test**: Launch app, verify menu displays, navigate options, exit cleanly

### Tests for User Story 6 (Red Phase)

- [x] T074 [P] [US6] Write test_display_menu in tests/test_ui.py
- [x] T075 [P] [US6] Write test_get_menu_choice_valid in tests/test_ui.py
- [x] T076 [P] [US6] Write test_get_menu_choice_invalid in tests/test_ui.py
- [x] T077 [US6] Write test_display_welcome_message in tests/test_ui.py
- [x] T078 [US6] Write test_display_goodbye_message in tests/test_ui.py
- [x] T079 [US6] Write test_display_error_message in tests/test_ui.py

### Implementation for User Story 6 (Green Phase)

- [x] T080 [US6] Implement display_welcome_message() in phase-1-console/src/todo/ui.py
- [x] T081 [US6] Implement display_menu() in phase-1-console/src/todo/ui.py
- [x] T082 [US6] Implement get_menu_choice() with validation in phase-1-console/src/todo/ui.py
- [x] T083 [US6] Implement display_goodbye_message() with data warning in phase-1-console/src/todo/ui.py
- [x] T084 [US6] Implement display_error_message() in phase-1-console/src/todo/ui.py
- [x] T085 [US6] Verify tests pass (Green): `uv run pytest -k "menu or welcome or goodbye or error_message"`

**Checkpoint**: All UI components ready for main loop integration

---

## Phase 9: Integration (Main Loop)

**Purpose**: Wire everything together in main.py

### Tests for Integration (Red Phase)

- [x] T086 [P] Write test_main_loop_exit in tests/test_main.py
- [x] T087 [P] Write test_main_loop_keyboard_interrupt in tests/test_main.py

### Implementation for Integration (Green Phase)

- [x] T088 Create main() function in phase-1-console/src/todo/main.py
- [x] T089 Implement main loop with menu dispatch in phase-1-console/src/todo/main.py
- [x] T090 Add KeyboardInterrupt (Ctrl+C) handling in phase-1-console/src/todo/main.py
- [x] T091 Add entry point to pyproject.toml for `uv run todo`
- [x] T092 Verify all tests pass: `uv run pytest`

**Checkpoint**: Application fully functional and testable end-to-end

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [x] T093 Run full test suite and verify 100% pass rate: `uv run pytest -v`
- [x] T094 [P] Verify PEP 8 compliance (line length, imports, naming)
- [x] T095 [P] Verify all functions have type hints
- [x] T096 [P] Verify all public functions have docstrings
- [x] T097 Create README.md with setup and usage instructions in phase-1-console/
- [x] T098 Run manual acceptance test per quickstart.md scenarios
- [x] T099 Verify edge cases per spec.md (200 char title, 1000 char description, Ctrl+C, empty list operations)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in priority order (P1 → P2 → P3 → P4 → P5 → P6)
  - Some parallelization possible (tests within a story)
- **Integration (Phase 9)**: Depends on all user stories completing
- **Polish (Phase 10)**: Depends on Integration completing

### User Story Dependencies

| Story | Depends On | Notes |
|-------|------------|-------|
| US1 (View) | Foundational | Foundation only - MVP starting point |
| US2 (Add) | Foundational | Uses Task model from Foundation |
| US3 (Complete) | Foundational | Uses get_task, adds toggle_complete |
| US4 (Update) | Foundational | Uses get_task, adds update_task |
| US5 (Delete) | Foundational | Uses get_task, adds delete_task |
| US6 (Menu/Exit) | Foundational | UI only, no manager dependencies |

### Within Each User Story (TDD Cycle)

1. Write tests (Red) - MUST fail before implementation
2. Implement minimal code (Green) - MUST pass tests
3. Refactor if needed - MUST keep tests green

### Parallel Opportunities

**Phase 1 (Setup)**:
- T004, T005 can run in parallel (different directories)

**Phase 2 (Foundational)**:
- T006, T007 can run in parallel (different test files)

**Each User Story Tests**:
- All test tasks marked [P] can run in parallel (independent test cases)

**Each User Story Implementation**:
- Follow sequential order within story (tests → models → services → UI)

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together (Red Phase):
Task T027: "test_add_task_returns_task_with_id"
Task T028: "test_add_task_sequential_ids"
Task T029: "test_add_task_with_description"
Task T030: "test_add_task_empty_title_raises_error"
Task T031: "test_add_task_title_too_long_raises_error"
Task T032: "test_add_task_description_too_long_raises_error"

# After tests written, implement sequentially:
Task T035: validation logic
Task T036: validation logic
Task T037: add_task method (depends on T035, T036)
Task T038-T040: UI functions
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (View)
4. **STOP and VALIDATE**: Test viewing empty list and with tasks
5. This alone delivers value - users can see their task list

### Incremental Delivery

| After Phase | User Can... | Value Delivered |
|-------------|-------------|-----------------|
| 3 (US1) | View tasks | See what's in the list |
| 4 (US2) | Add tasks | Create their todo items |
| 5 (US3) | Mark complete | Track progress |
| 6 (US4) | Update tasks | Refine task details |
| 7 (US5) | Delete tasks | Clean up list |
| 8 (US6) | Navigate/Exit | Full menu interaction |
| 9 (Integration) | Run full app | End-to-end experience |

### Suggested MVP Scope

**Minimum**: Phase 1-3 (Setup + Foundational + US1 View)
**Recommended**: Phase 1-5 (Setup + Foundational + US1-US3 View/Add/Complete)

---

## Summary

| Category | Count |
|----------|-------|
| Total Tasks | 99 |
| Setup Tasks | 5 |
| Foundational Tasks | 8 |
| US1 (View) Tasks | 13 |
| US2 (Add) Tasks | 15 |
| US3 (Complete) Tasks | 10 |
| US4 (Update) Tasks | 12 |
| US5 (Delete) Tasks | 10 |
| US6 (Menu/Exit) Tasks | 12 |
| Integration Tasks | 7 |
| Polish Tasks | 7 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- TDD is NON-NEGOTIABLE per Constitution Principle III
- All tests MUST fail before implementation (Red phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
