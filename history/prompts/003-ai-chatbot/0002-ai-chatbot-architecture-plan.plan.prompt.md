---
id: "0002"
title: "AI Chatbot Architecture Plan"
stage: plan
date: 2025-12-03
surface: agent
model: claude-opus-4-5-20251101
feature: 003-ai-chatbot
branch: 003-ai-chatbot
user: dell
command: /sp.plan
labels: ["architecture", "chatkit", "agents-sdk", "mcp", "streaming"]
links:
  spec: specs/003-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-chatbot/plan.md
  - specs/003-ai-chatbot/research.md
  - specs/003-ai-chatbot/data-model.md
  - specs/003-ai-chatbot/quickstart.md
  - specs/003-ai-chatbot/contracts/chat-api.yaml
tests:
  - null
---

## Prompt

/sp.plan (execute implementation planning for 003-ai-chatbot feature)

## Response snapshot

Created comprehensive implementation plan for AI-Powered Todo Chatbot:

**Artifacts Generated:**
- `plan.md` - Full implementation plan with architecture, phases, decisions
- `research.md` - Phase 0 research on SDKs, patterns, streaming
- `data-model.md` - Conversation and Message entity definitions
- `contracts/chat-api.yaml` - OpenAPI 3.1 spec for chat endpoints
- `quickstart.md` - Setup and verification guide

**Key Architecture Decisions:**
1. Service layer extraction (shared by MCP and REST)
2. Model factory pattern (OpenAI/Gemini abstraction)
3. In-process MCP tools (function_tool pattern)
4. Stateless chat with DB persistence
5. SSE streaming via FastAPI StreamingResponse

**Implementation Phases (7 total):**
- Phase A: Service layer foundation
- Phase B: Database models (Conversation, Message)
- Phase C: MCP tools (5 tools)
- Phase D: Agent integration (Agents SDK)
- Phase E: Chat API endpoint
- Phase F: Frontend ChatKit
- Phase G: Testing & polish

**Constitution Check:** All 6 principles PASSED

## Outcome

- Impact: Complete technical architecture for Phase 3 AI chatbot
- Tests: N/A (planning phase)
- Files: 5 files created (plan, research, data-model, quickstart, API contract)
- Next prompts: /sp.tasks for task generation
- Reflection: Architecture leverages existing Phase 2 patterns while adding AI capabilities

## Evaluation notes (flywheel)

- Failure modes observed: None - all gates passed
- Graders run and results (PASS/FAIL): Constitution Check PASS (6/6 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
