# Data Model: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2025-12-03

## Entity Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      User       │     │   Conversation  │     │     Message     │
│  (Better Auth)  │────<│                 │────<│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│      Task       │
│   (Existing)    │
└─────────────────┘
```

## New Entities

### Conversation

Represents a chat session belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Unique identifier |
| user_id | String | FK (Better Auth), Index, NOT NULL | Owner of conversation |
| created_at | DateTime | NOT NULL, Default: now() | When conversation started |
| updated_at | DateTime | NOT NULL, Default: now() | Last activity timestamp |

**Relationships**:
- One User has Many Conversations
- One Conversation has Many Messages

**Indexes**:
- `idx_conversations_user_id` on `user_id`
- `idx_conversations_updated_at` on `updated_at` (for sorting recent)

**SQLModel Definition**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
```

### Message

Represents a single message within a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Unique identifier |
| conversation_id | Integer | FK (Conversation), Index, NOT NULL | Parent conversation |
| user_id | String | Index, NOT NULL | Message owner (denormalized) |
| role | String | NOT NULL, Enum: "user", "assistant" | Who sent the message |
| content | Text | NOT NULL | Message content |
| tool_calls | JSON | NULL | MCP tools invoked (assistant only) |
| created_at | DateTime | NOT NULL, Default: now() | When message was sent |

**Relationships**:
- One Conversation has Many Messages
- Messages ordered by `created_at` within conversation

**Indexes**:
- `idx_messages_conversation_id` on `conversation_id`
- `idx_messages_user_id` on `user_id`
- `idx_messages_created_at` on `created_at`

**SQLModel Definition**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str
    tool_calls: dict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utc_now, index=True)
```

## Existing Entities (Reference)

### Task (Existing - No Changes)

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | PK |
| user_id | String | Owner |
| title | String(200) | Task title |
| description | String(1000) | Optional description |
| completed | Boolean | Completion status |
| color | String(20) | Note color |
| pinned | Boolean | Pinned status |
| archived | Boolean | Archive status |
| deleted_at | DateTime | Soft delete |
| reminder_at | DateTime | Reminder time |
| created_at | DateTime | Creation time |
| updated_at | DateTime | Last update |

## State Transitions

### Conversation States

```
[New] ──create──> [Active] ──idle (30 days)──> [Archived]
                     │
                     └──delete──> [Deleted]
```

Note: Archival/deletion are future considerations. Current scope: Active only.

### Message States

Messages are immutable once created. No state transitions.

## Validation Rules

### Conversation
- `user_id`: Must be non-empty string
- `created_at`: Must be <= `updated_at`

### Message
- `conversation_id`: Must reference existing Conversation
- `user_id`: Must match parent Conversation's `user_id`
- `role`: Must be "user" or "assistant"
- `content`: Must be non-empty string
- `tool_calls`: Valid JSON if present (assistant messages only)

## Database Migration

### SQL (for reference)

```sql
-- conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);

-- messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

### SQLModel Auto-Migration

With `SQLModel.metadata.create_all()`, tables will be created automatically on first run. For production, use Alembic migrations.

## Query Patterns

### Load Conversation with Messages

```python
async def get_conversation_with_messages(
    session: AsyncSession,
    user_id: str,
    conversation_id: int
) -> tuple[Conversation, list[Message]]:
    # Get conversation (verify ownership)
    conversation = await session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise NotFoundError("Conversation not found")

    # Get messages ordered by time
    result = await session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = result.all()

    return conversation, messages
```

### Create New Conversation

```python
async def create_conversation(
    session: AsyncSession,
    user_id: str
) -> Conversation:
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation
```

### Add Message to Conversation

```python
async def add_message(
    session: AsyncSession,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_calls: dict | None = None
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    session.add(message)

    # Update conversation timestamp
    conversation = await session.get(Conversation, conversation_id)
    conversation.updated_at = _utc_now()

    await session.commit()
    await session.refresh(message)
    return message
```

### List User's Conversations

```python
async def list_conversations(
    session: AsyncSession,
    user_id: str,
    limit: int = 20
) -> list[Conversation]:
    result = await session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    return result.all()
```
