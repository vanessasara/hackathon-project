# Implementation Plan: Console Todo App

**Branch**: `001-console-todo-app` | **Date**: 2025-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

## Summary

Build an in-memory Python console Todo application with an interactive numbered menu interface. The application provides 5 core operations (add, view, update, delete, mark complete) with input validation, helpful error messages, and a clean exit flow. Data is stored in-memory using Python's standard library; no persistence across sessions.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only); pytest for testing
**Storage**: In-memory (Python list with Task dataclass instances)
**Testing**: pytest with TDD Red-Green-Refactor cycle
**Target Platform**: Terminal/console (Linux, macOS, Windows)
**Project Type**: Single project (console CLI application)
**Performance Goals**: View tasks < 2 seconds, add task < 30 seconds user flow
**Constraints**: No external dependencies, in-memory only, single-user
**Scale/Scope**: Single user, ~100 tasks typical, no pagination required

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Spec-Driven Development | Spec exists before implementation | ✅ PASS | spec.md complete with 6 user stories |
| II. Clean Code | PEP 8, type hints, docstrings | ✅ PLAN | Will enforce in all generated code |
| III. Test-First Development | TDD Red-Green-Refactor | ✅ PLAN | pytest tests before implementation |
| IV. Single Responsibility | Separate models, manager, UI | ✅ PLAN | 4 modules planned (models, manager, ui, main) |
| V. Evolutionary Architecture | In-memory with abstraction | ✅ PLAN | TaskManager abstracts storage; swappable later |
| VI. User Experience First | Clear prompts, error messages | ✅ PLAN | All acceptance scenarios define UX requirements |

**Pre-Design Gate**: ✅ PASSED - All principles addressed in plan

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (phase-1-console/)

```text
phase-1-console/
├── pyproject.toml       # UV project configuration
├── README.md            # Setup and usage instructions
├── src/
│   └── todo/
│       ├── __init__.py  # Package initialization
│       ├── main.py      # Entry point with main loop
│       ├── models.py    # Task dataclass definition
│       ├── manager.py   # TaskManager business logic
│       └── ui.py        # Menu display and input handling
└── tests/
    ├── __init__.py
    ├── test_models.py   # Task model unit tests
    ├── test_manager.py  # TaskManager unit tests
    └── test_ui.py       # UI function tests (input/output)
```

**Structure Decision**: Single project structure selected. The application is a console CLI with clear separation of concerns:
- `models.py`: Data structures (Task dataclass)
- `manager.py`: Business logic (CRUD operations, validation)
- `ui.py`: Presentation (menu display, input prompts, formatting)
- `main.py`: Application entry point and main loop

This separation supports Constitution Principle IV (Single Responsibility) and enables independent testing per Constitution Principle III.

## Complexity Tracking

> No violations. Design follows all Constitution principles without exceptions.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
