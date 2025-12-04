# Phase 3: AI-Powered Todo Chatbot

## Project Overview

This is Phase 3 of the Evolution of Todo hackathon project. It extends Phase 2 with AI-powered natural language task management using ChatKit.

## Features

- **Natural Language Task Management**: Add, list, complete, delete, and update tasks via chat
- **Conversation Persistence**: All chat history stored in database
- **Stateless Architecture**: Server restarts don't lose conversation context
- **Streaming Responses**: Real-time SSE streaming for smooth UX
- **Multi-Provider Support**: OpenAI and Gemini via unified factory

## Architecture

- **Frontend**: Next.js 16 with ChatKit UI
- **Backend**: FastAPI with OpenAI Agents SDK and MCP tools
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT verification

## Quick Start

### Prerequisites

- Node.js 22+ (frontend)
- Python 3.13+ (backend)
- Neon PostgreSQL database
- OpenAI API key or Gemini API key

### Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env and add your database URL and API keys

# Start server
uv run uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your database URL and auth secret

# Start dev server
pnpm dev
```

## API Endpoints

### Chat Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/chat | Send chat message (SSE streaming) | Yes |
| GET | /api/chat/conversations | List user's conversations | Yes |
| GET | /api/chat/conversations/{id} | Get conversation with messages | Yes |
| DELETE | /api/chat/conversations/{id} | Delete conversation | Yes |

### Chat Request Example

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

### SSE Response Format

```text
data: {"type": "text_delta", "content": "I've added"}
data: {"type": "text_delta", "content": " 'Buy groceries'"}
data: {"type": "done", "conversation_id": 42, "tool_calls": []}
```

## MCP Tools

The agent has access to 5 MCP tools:

1. **add_task** - Create new tasks
2. **list_tasks** - List tasks with status filter
3. **complete_task** - Toggle task completion
4. **delete_task** - Soft delete tasks
5. **update_task** - Update task title/description

## Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://...

# Authentication
BETTER_AUTH_URL=http://localhost:3000

# AI Provider
LLM_PROVIDER=openai  # or "gemini"
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# GEMINI_API_KEY=...
# GEMINI_DEFAULT_MODEL=gemini-2.0-flash
```

### Frontend (.env.local)

```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHATKIT_API_URL=/api/chat
```

## Project Structure

```
phase-3-chatbot/
├── backend/
│   └── src/
│       ├── agents/          # AI agents
│       │   ├── factory.py   # Model factory (OpenAI/Gemini)
│       │   └── todo_agent.py # TodoAgent with MCP tools
│       ├── mcp/             # MCP tools
│       │   └── tools.py     # 5 task management tools
│       ├── models/          # SQLModel models
│       │   ├── conversation.py
│       │   └── message.py
│       ├── services/        # Business logic layer
│       │   ├── task_service.py
│       │   └── conversation_service.py
│       ├── routers/         # API endpoints
│       │   └── chat.py      # Chat SSE endpoint
│       └── schemas/         # Pydantic schemas
│           └── chat.py
└── frontend/
    └── src/
        └── app/
            └── chat/        # Chat page (TODO)
                └── page.tsx
```

## Testing

```bash
# Backend tests
cd backend
pytest -v

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

## Development Notes

- Agent uses singleton pattern for efficiency
- All conversations persisted to database (stateless backend)
- SSE streaming for real-time response
- Service layer shared by REST endpoints and MCP tools
- Multi-provider support via factory pattern

## Phase 2 Features (Inherited)

All Phase 2 features are preserved:
- Task CRUD operations
- Label management
- Image attachments (Cloudflare R2)
- Google Keep-style UI
- Better Auth authentication

## License

MIT
