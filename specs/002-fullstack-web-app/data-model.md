# Data Model: Full-Stack Web Todo Application

**Feature**: 002-fullstack-web-app
**Date**: 2025-12-02

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA MODEL                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────┐         ┌─────────────────────────────────┐   │
│  │       USER          │         │            TASK                  │   │
│  ├─────────────────────┤         ├─────────────────────────────────┤   │
│  │ id: string (PK)     │ 1     * │ id: serial (PK)                 │   │
│  │ email: string (UQ)  │─────────│ user_id: string (FK)            │   │
│  │ name: string        │         │ title: varchar(200)             │   │
│  │ image: string?      │         │ description: text?              │   │
│  │ email_verified: bool│         │ completed: boolean              │   │
│  │ created_at: datetime│         │ created_at: datetime            │   │
│  │ updated_at: datetime│         │ updated_at: datetime            │   │
│  └─────────────────────┘         └─────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────┐         ┌─────────────────────────────────┐   │
│  │      SESSION        │         │          ACCOUNT                │   │
│  ├─────────────────────┤         ├─────────────────────────────────┤   │
│  │ id: string (PK)     │         │ id: string (PK)                 │   │
│  │ user_id: string (FK)│         │ user_id: string (FK)            │   │
│  │ token: string (UQ)  │         │ account_id: string              │   │
│  │ expires_at: datetime│         │ provider_id: string             │   │
│  │ ip_address: string? │         │ access_token: text?             │   │
│  │ user_agent: string? │         │ refresh_token: text?            │   │
│  │ created_at: datetime│         │ created_at: datetime            │   │
│  │ updated_at: datetime│         │ updated_at: datetime            │   │
│  └─────────────────────┘         └─────────────────────────────────┘   │
│                                                                          │
│  Note: USER, SESSION, ACCOUNT managed by Better Auth                     │
│        TASK is application-specific                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Entities

### User (Managed by Better Auth)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string | PK | Unique identifier (cuid) |
| email | varchar(255) | NOT NULL, UNIQUE | User's email address |
| name | text | - | Display name |
| image | text | - | Profile image URL |
| email_verified | boolean | DEFAULT false | Email verification status |
| created_at | timestamp | DEFAULT now() | Creation timestamp |
| updated_at | timestamp | DEFAULT now() | Last update timestamp |

### Session (Managed by Better Auth)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string | PK | Session identifier |
| user_id | string | FK -> user.id | Owner of session |
| token | string | NOT NULL, UNIQUE | Session token (in cookie) |
| expires_at | timestamp | NOT NULL | Session expiration |
| ip_address | text | - | Client IP address |
| user_agent | text | - | Client user agent |
| created_at | timestamp | DEFAULT now() | Creation timestamp |
| updated_at | timestamp | DEFAULT now() | Last update timestamp |

### Account (Managed by Better Auth)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string | PK | Account identifier |
| user_id | string | FK -> user.id | Owner of account |
| account_id | string | NOT NULL | Provider account ID |
| provider_id | string | NOT NULL | Provider name (credential, google, etc.) |
| access_token | text | - | OAuth access token |
| refresh_token | text | - | OAuth refresh token |
| expires_at | timestamp | - | Token expiration |
| created_at | timestamp | DEFAULT now() | Creation timestamp |
| updated_at | timestamp | DEFAULT now() | Last update timestamp |

### Task (Application Entity)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | serial | PK | Auto-increment ID |
| user_id | string | FK -> user.id, NOT NULL | Owner of task |
| title | varchar(200) | NOT NULL | Task title (1-200 chars) |
| description | text | - | Optional description (max 1000 chars) |
| completed | boolean | NOT NULL, DEFAULT false | Completion status |
| created_at | timestamp | NOT NULL, DEFAULT now() | Creation timestamp |
| updated_at | timestamp | NOT NULL, DEFAULT now() | Last update timestamp |

**Indexes**:
- `tasks_user_id_idx` on `user_id` (for filtering by user)
- `tasks_completed_idx` on `completed` (for filtering by status)

## Validation Rules

### Task Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| title | Required | "Title is required" |
| title | Min 1 char | "Title cannot be empty" |
| title | Max 200 chars | "Title cannot exceed 200 characters" |
| description | Max 1000 chars | "Description cannot exceed 1000 characters" |

### User Validation (Better Auth)

| Field | Rule | Error Message |
|-------|------|---------------|
| email | Required | "Email is required" |
| email | Valid format | "Invalid email format" |
| email | Unique | "Email already in use" |
| password | Min 8 chars | "Password must be at least 8 characters" |

## State Transitions

### Task States

```
┌──────────────────────────────────────────────────┐
│                 TASK LIFECYCLE                    │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────┐     create      ┌─────────────┐    │
│  │ (none)  │ ───────────────►│ INCOMPLETE  │    │
│  └─────────┘                 └──────┬──────┘    │
│                                     │            │
│                          toggle     │  toggle    │
│                       ┌─────────────┴──────┐     │
│                       │                    │     │
│                       ▼                    │     │
│                 ┌───────────┐              │     │
│                 │ COMPLETED │◄─────────────┘     │
│                 └─────┬─────┘                    │
│                       │                          │
│                 delete│                          │
│                       ▼                          │
│                 ┌───────────┐                    │
│                 │ (deleted) │                    │
│                 └───────────┘                    │
│                                                   │
└──────────────────────────────────────────────────┘
```

## Drizzle Schema (TypeScript)

```typescript
// drizzle/schema.ts
import { pgTable, serial, text, varchar, boolean, timestamp, index } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Better Auth generates user, session, account tables
// This is the application-specific task table

export const tasks = pgTable(
  "tasks",
  {
    id: serial("id").primaryKey(),
    userId: text("user_id").notNull(),
    title: varchar("title", { length: 200 }).notNull(),
    description: text("description"),
    completed: boolean("completed").notNull().default(false),
    createdAt: timestamp("created_at").notNull().defaultNow(),
    updatedAt: timestamp("updated_at").notNull().defaultNow(),
  },
  (table) => ({
    userIdIdx: index("tasks_user_id_idx").on(table.userId),
    completedIdx: index("tasks_completed_idx").on(table.completed),
  })
);

export type Task = typeof tasks.$inferSelect;
export type NewTask = typeof tasks.$inferInsert;
```

## SQLModel Schema (Python)

```python
# models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```
