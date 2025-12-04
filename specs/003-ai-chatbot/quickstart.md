# Quickstart: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2025-12-03

## Prerequisites

- Phase 2 backend running (`phase-3-chatbot/backend`)
- Phase 2 frontend running (`phase-3-chatbot/frontend`)
- Neon PostgreSQL database configured
- Better Auth working (user can log in)
- OpenAI API key OR Gemini API key

## Setup Steps

### 1. Backend Dependencies

```bash
cd phase-3-chatbot/backend

# Add new dependencies
uv add openai-agents mcp

# Verify installation
uv pip list | grep -E "(openai|mcp)"
```

### 2. Environment Variables

Add to `phase-3-chatbot/backend/.env`:

```env
# AI Provider (choose one)
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# OR Gemini Configuration
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=your-gemini-key
# GEMINI_DEFAULT_MODEL=gemini-2.0-flash
```

Add to `phase-3-chatbot/frontend/.env.local`:

```env
NEXT_PUBLIC_CHATKIT_API_URL=/api/chat
```

### 3. Database Tables

Tables will be auto-created by SQLModel on first run. Alternatively:

```bash
# Connect to Neon and run:
psql $DATABASE_URL -f scripts/create_chat_tables.sql
```

### 4. Start Backend

```bash
cd phase-3-chatbot/backend
source .venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

Verify chat endpoint:
```bash
# Get JWT token from frontend login, then:
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you help me with?"}'
```

### 5. Start Frontend

```bash
cd phase-3-chatbot/frontend
pnpm dev
```

Navigate to: `http://localhost:3000/chat`

## Verification Checklist

- [ ] Backend starts without errors
- [ ] `/api/health` returns 200
- [ ] Chat endpoint accepts messages
- [ ] Streaming response works
- [ ] Tasks can be created via chat
- [ ] Conversations persist in database
- [ ] Frontend ChatKit renders

## Test Commands

Try these in the chat:

| Command | Expected Result |
|---------|-----------------|
| "Add a task to buy groceries" | Creates task, confirms creation |
| "Show me all my tasks" | Lists all tasks |
| "What's pending?" | Lists pending tasks only |
| "Mark task 1 as complete" | Marks task complete |
| "Delete the groceries task" | Deletes matching task |
| "Update task 1 to 'Call mom tonight'" | Updates task title |

## Troubleshooting

### Chat returns 401
- Check JWT token is valid
- Verify `BETTER_AUTH_URL` in backend `.env`

### No response from agent
- Check `OPENAI_API_KEY` is set
- Verify `LLM_PROVIDER` matches your key
- Check backend logs for API errors

### Tasks not saving
- Verify `DATABASE_URL` is correct
- Check database connection logs

### Streaming not working
- Ensure browser supports SSE
- Check CORS settings allow streaming

## Architecture Reference

```
Frontend                    Backend
   │                           │
   │  POST /api/chat           │
   │  {message: "..."}         │
   │ ─────────────────────────>│
   │                           │
   │  SSE: text_delta events   │
   │ <─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
   │                           │
   │  SSE: done event          │
   │ <─────────────────────────│
   │                           │
```

## Next Steps

After quickstart verification:

1. Run `/sp.tasks` to generate implementation tasks
2. Follow TDD workflow (Red → Green → Refactor)
3. Run `pytest -v` after each implementation
4. Commit after each passing test suite
