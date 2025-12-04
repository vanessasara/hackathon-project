# Research: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2025-12-03
**Status**: Complete

## Research Topics

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK with `function_tool` decorator for MCP tools

**Rationale**:
- Official SDK provides structured tool calling
- `Runner.run_streamed()` enables SSE streaming
- Model factory pattern allows provider switching (OpenAI/Gemini)
- Tools defined as Python functions with type hints

**Alternatives Considered**:
- Direct OpenAI API calls: Rejected - requires manual tool orchestration
- LangChain: Rejected - over-engineered for this use case
- Custom agent loop: Rejected - reinventing the wheel

**Implementation Pattern**:
```python
from agents import Agent, Runner, function_tool

@function_tool
def add_task(user_id: str, title: str, description: str | None = None) -> dict:
    """Add a new task for the user."""
    return task_service.create_task(user_id, title, description)

agent = Agent(
    name="TodoAgent",
    model=create_model(),
    instructions="You help users manage their todo list...",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)

result = Runner.run_streamed(starting_agent=agent, input=user_message)
```

### 2. MCP Tools Design

**Decision**: In-process MCP tools using `function_tool` pattern (not subprocess)

**Rationale**:
- Lower latency (no IPC overhead)
- Shared database session context
- Simpler deployment (single process)
- Easier debugging

**Alternatives Considered**:
- stdio subprocess MCP: Rejected - adds latency and complexity
- HTTP MCP server: Rejected - unnecessary network hop

**Tool Specifications**:

| Tool | Parameters | Returns | Service Method |
|------|------------|---------|----------------|
| `add_task` | user_id, title, description? | {task_id, status, title} | task_service.create_task() |
| `list_tasks` | user_id, status? | [{id, title, completed}...] | task_service.list_tasks() |
| `complete_task` | user_id, task_id | {task_id, status, title} | task_service.toggle_complete() |
| `delete_task` | user_id, task_id | {task_id, status, title} | task_service.delete_task() |
| `update_task` | user_id, task_id, title?, description? | {task_id, status, title} | task_service.update_task() |

### 3. Streaming Architecture

**Decision**: Server-Sent Events (SSE) for streaming responses

**Rationale**:
- Native browser support
- One-way server-to-client (fits chat model)
- FastAPI `StreamingResponse` built-in support
- ChatKit expects streaming responses

**Alternatives Considered**:
- WebSockets: Rejected - bidirectional not needed, more complex
- Long polling: Rejected - inefficient, poor UX
- HTTP/2 server push: Rejected - limited browser support

**Implementation Pattern**:
```python
from fastapi.responses import StreamingResponse

async def stream_chat_response(agent, user_message):
    result = Runner.run_streamed(starting_agent=agent, input=user_message)
    async for event in result:
        if event.type == "text_delta":
            yield f"data: {json.dumps({'content': event.text})}\n\n"
    yield f"data: {json.dumps({'done': True})}\n\n"

@router.post("/api/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_current_user)):
    return StreamingResponse(
        stream_chat_response(agent, request.message),
        media_type="text/event-stream"
    )
```

### 4. Conversation Persistence

**Decision**: Database-first stateless architecture

**Rationale**:
- Hackathon requirement (stateless server)
- Enables horizontal scaling
- Survives server restarts
- Clean separation of concerns

**Alternatives Considered**:
- In-memory with Redis cache: Rejected - still needs persistence
- File-based storage: Rejected - not scalable
- Session storage: Rejected - lost on restart

**Flow**:
1. Receive chat request with optional `conversation_id`
2. If no `conversation_id`: create new Conversation
3. Load all Messages for conversation from DB
4. Build message array for agent
5. Save user message to DB
6. Run agent, stream response
7. Save assistant message to DB
8. Return `conversation_id` for continuation

### 5. Model Factory Pattern

**Decision**: Centralized factory with environment-based provider selection

**Rationale**:
- Single point for model configuration
- Easy provider switching (OpenAI ↔ Gemini)
- No hardcoded API keys in code
- Testable (can mock factory)

**Implementation Pattern**:
```python
# agents/factory.py
import os
from openai import AsyncOpenAI

def create_model():
    provider = os.getenv("LLM_PROVIDER", "openai")

    if provider == "gemini":
        return AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    # Default: OpenAI
    return os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
```

### 6. ChatKit Frontend Integration

**Decision**: Custom backend mode with JWT authentication

**Rationale**:
- Full control over agent logic
- Integrates with existing Better Auth
- No Agent Builder dependency

**Implementation Pattern**:
```tsx
// components/chatkit/ChatKitWidget.tsx
const client = createChatKitClient({
  api: {
    url: process.env.NEXT_PUBLIC_CHATKIT_API_URL,
    fetch: async (url, options) => {
      const session = await getSession();
      return fetch(url, {
        ...options,
        headers: {
          ...options?.headers,
          Authorization: `Bearer ${session?.accessToken}`,
        },
      });
    },
  },
});
```

### 7. Service Layer Design

**Decision**: Extract CRUD logic into service layer with async session management

**Rationale**:
- MCP tools and REST endpoints share logic
- Single source of truth
- Testable in isolation
- Clear dependency injection

**Implementation Pattern**:
```python
# services/task_service.py
from sqlmodel.ext.asyncio.session import AsyncSession

async def create_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str | None = None
) -> Task:
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

## Research Summary

All technical unknowns have been resolved:

| Topic | Decision | Confidence |
|-------|----------|------------|
| Agent SDK | OpenAI Agents SDK with function_tool | High |
| MCP Pattern | In-process, direct service calls | High |
| Streaming | SSE via FastAPI StreamingResponse | High |
| Persistence | Database-first, stateless server | High |
| Model Factory | Environment-based provider selection | High |
| Frontend | ChatKit custom backend mode | High |
| Service Layer | Async services with session injection | High |

**Ready for Phase 1: Design & Contracts**
