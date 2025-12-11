# Data Model: Cloud Deployment

**Feature**: 005-cloud-deployment
**Date**: 2025-12-04

## Overview

This feature is infrastructure-focused and does not introduce new application data models. The existing Phase 4 data models remain unchanged.

## Infrastructure Entities

### Helm Values Configuration

The deployment is configured via Helm values. Key configuration entities:

```yaml
# Entity: ReplicaCount
replicaCount:
  frontend: 1    # Number of frontend pods
  backend: 1     # Number of backend pods

# Entity: Image
image:
  frontend:
    repository: string  # Container registry path
    tag: string         # Image version tag
    pullPolicy: string  # IfNotPresent | Always | Never
  backend:
    repository: string
    tag: string
    pullPolicy: string

# Entity: Service
service:
  frontend:
    type: string      # NodePort | LoadBalancer | ClusterIP
    port: number      # Service port
    nodePort: number  # External port (30000-32767)
  backend:
    type: string
    port: number

# Entity: Resources
resources:
  frontend:
    requests: { memory: string, cpu: string }
    limits: { memory: string, cpu: string }
  backend:
    requests: { memory: string, cpu: string }
    limits: { memory: string, cpu: string }

# Entity: Secrets
secrets:
  DATABASE_URL: string
  BETTER_AUTH_SECRET: string
  OPENAI_API_KEY: string
```

### GitHub Workflow Configuration

```yaml
# Entity: WorkflowTrigger
on:
  push:
    branches: [main]
  workflow_dispatch: {}

# Entity: DeploymentStep
steps:
  - checkout: boolean
  - doctl_auth: { token: secret_ref }
  - registry_login: { expiry: number }
  - build_push: { image: string, tag: string }
  - helm_deploy: { release: string, chart: string, values: string }
```

## Data Flow

```
GitHub Push → GitHub Actions → Build Images → Push to DO Registry
                    ↓
              doctl auth → kubectl config → Helm upgrade
                    ↓
              DOKS Cluster → Pull Images → Run Pods
                    ↓
              Pods → Connect to Neon PostgreSQL (external)
```

## State Transitions

### Deployment State Machine

```
┌─────────────┐
│   Idle      │
└──────┬──────┘
       │ push to main
       ▼
┌─────────────┐
│  Building   │ → Build failure → Idle (with error notification)
└──────┬──────┘
       │ build success
       ▼
┌─────────────┐
│  Pushing    │ → Push failure → Idle (with error notification)
└──────┬──────┘
       │ push success
       ▼
┌─────────────┐
│  Deploying  │ → Deploy failure → Idle (with error notification)
└──────┬──────┘
       │ deploy success
       ▼
┌─────────────┐
│  Running    │
└─────────────┘
```

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| ReplicaCount | frontend/backend | >= 1, integer |
| Service | nodePort | 30000-32767 |
| Resources | memory | Valid K8s quantity (e.g., "256Mi") |
| Resources | cpu | Valid K8s quantity (e.g., "100m") |
| Secrets | * | Non-empty when deployed |

## No New Application Entities (Basic Deployment)

This deployment feature does not modify:
- Task model (existing in Phase 4)
- User model (existing in Phase 4)
- Session model (existing in Phase 4)
- Chat history (existing in Phase 4)

All application data remains in Neon PostgreSQL, accessed via existing connection string.

---

## Part B: Advanced Features Data Model

The advanced features (reminders, notifications, recurring tasks) require extensions to existing models and new entities.

---

## Extended Task Model

The existing `Task` model is extended with new fields for reminders and recurrence:

```python
class Task(SQLModel, table=True):
    """Extended Task model with reminder and recurrence support."""

    __tablename__ = "tasks"

    # Existing fields (Phase 4)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    color: str = Field(default="default", max_length=20)
    pinned: bool = Field(default=False)
    archived: bool = Field(default=False, index=True)
    deleted_at: Optional[datetime] = Field(default=None, index=True)
    reminder_at: Optional[datetime] = Field(default=None, index=True)  # Exists
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    # NEW: Reminder tracking
    reminder_sent: bool = Field(
        default=False,
        index=True,
        description="Whether reminder notification was sent"
    )

    # NEW: Due date (separate from reminder)
    due_at: Optional[datetime] = Field(
        default=None,
        index=True,
        description="Task due date/time (deadline)"
    )

    # NEW: Recurring task fields
    is_recurring: bool = Field(
        default=False,
        index=True,
        description="Whether this is a recurring task"
    )
    recurrence_rule: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Recurrence pattern: daily, weekly, monthly, weekdays, or cron expression"
    )
    recurrence_end: Optional[datetime] = Field(
        default=None,
        description="When recurring task should stop creating new occurrences"
    )
    parent_task_id: Optional[int] = Field(
        default=None,
        foreign_key="tasks.id",
        index=True,
        description="ID of original recurring task (for generated occurrences)"
    )
```

### Field Descriptions

| Field | Type | Purpose |
|-------|------|---------|
| `reminder_sent` | bool | Prevents duplicate notifications; set to true after delivery |
| `due_at` | datetime | Task deadline (separate from reminder time) |
| `is_recurring` | bool | Marks task as recurring template |
| `recurrence_rule` | str | Pattern: "daily", "weekly", "monthly", "weekdays", "cron:..." |
| `recurrence_end` | datetime | Optional end date for recurring series |
| `parent_task_id` | int | Links occurrence to original recurring task |

### Recurrence Rule Values

| Value | Description | Example |
|-------|-------------|---------|
| `daily` | Every day at same time | Daily standup |
| `weekly` | Every 7 days | Weekly review |
| `monthly` | Same day each month | Monthly report |
| `weekdays` | Monday through Friday | Work tasks |
| `cron:0 9 * * 1` | Custom cron expression | Every Monday 9am |

---

## New Entity: PushSubscription

Stores browser push notification subscriptions for users:

```python
class PushSubscription(SQLModel, table=True):
    """Browser push notification subscription."""

    __tablename__ = "push_subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="User ID from Better Auth")
    endpoint: str = Field(description="Push service endpoint URL")
    p256dh_key: str = Field(description="User's public key for encryption")
    auth_key: str = Field(description="Authentication secret")
    user_agent: Optional[str] = Field(default=None, description="Browser user agent")
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    class Config:
        # Unique constraint on user_id + endpoint
        table_args = (UniqueConstraint("user_id", "endpoint"),)
```

### Push Subscription Fields

| Field | Type | Purpose |
|-------|------|---------|
| `endpoint` | str | Browser push service URL (unique per browser) |
| `p256dh_key` | str | Public key for encrypting notification payload |
| `auth_key` | str | Shared secret for authentication |
| `user_agent` | str | Browser identification (for debugging) |

---

## Event Schemas (Kafka Messages)

### TaskEvent

Published to `task-events` topic on any task modification:

```python
class TaskEvent(BaseModel):
    """Event published when task is created, updated, completed, or deleted."""

    event_type: Literal["created", "updated", "completed", "deleted"]
    task_id: int
    user_id: str
    task_data: dict  # Full task serialization
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # For recurring task completion
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
```

### ReminderEvent

Published to `reminders` topic when reminder is due:

```python
class ReminderEvent(BaseModel):
    """Event published when a task reminder is due for delivery."""

    task_id: int
    user_id: str
    title: str
    reminder_at: datetime
    due_at: Optional[datetime] = None

    # Push subscription for notification delivery
    push_subscription: Optional[dict] = None  # endpoint, keys
```

### TaskUpdateEvent

Published to `task-updates` topic for real-time sync (future):

```python
class TaskUpdateEvent(BaseModel):
    """Event for real-time task synchronization across clients."""

    event_type: Literal["sync"]
    task_id: int
    user_id: str
    changes: dict  # Only changed fields
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## Dapr Component Entities

### PubSubComponent (Kafka)

```yaml
# Entity: DaprPubSubComponent
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    brokers: string           # Kafka bootstrap servers
    authType: string          # "password" for SASL
    saslUsername: secret_ref  # From Kubernetes secret
    saslPassword: secret_ref  # From Kubernetes secret
    saslMechanism: string     # "SCRAM-SHA-256"
```

### CronBindingComponent

```yaml
# Entity: DaprCronBinding
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
    schedule: string  # Cron expression: "*/1 * * * *"
  scopes:
    - string[]        # App IDs that receive triggers
```

---

## Data Flow Diagrams

### Reminder Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Task with   │     │   Backend    │     │   Kafka      │
│  reminder_at │────▶│  /check-     │────▶│  reminders   │
│  <= now      │     │  reminders   │     │  topic       │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser    │◀────│ Notification │◀────│  Consumer    │
│   Push API   │     │   Service    │     │  Group       │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Recurring Task Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Complete    │     │   Backend    │     │   Kafka      │
│  Recurring   │────▶│  publishes   │────▶│  task-events │
│  Task        │     │  event       │     │  topic       │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Next       │◀────│  Recurring   │◀────│  Consumer    │
│   Task       │     │  Task Svc    │     │  Group       │
│   Created    │     │  (Backend)   │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## Database Migrations Required

### Migration 001: Add reminder_sent field

```sql
ALTER TABLE tasks ADD COLUMN reminder_sent BOOLEAN DEFAULT FALSE;
CREATE INDEX ix_tasks_reminder_sent ON tasks(reminder_sent);
```

### Migration 002: Add due_at field

```sql
ALTER TABLE tasks ADD COLUMN due_at TIMESTAMP;
CREATE INDEX ix_tasks_due_at ON tasks(due_at);
```

### Migration 003: Add recurring task fields

```sql
ALTER TABLE tasks ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE;
ALTER TABLE tasks ADD COLUMN recurrence_rule VARCHAR(100);
ALTER TABLE tasks ADD COLUMN recurrence_end TIMESTAMP;
ALTER TABLE tasks ADD COLUMN parent_task_id INTEGER REFERENCES tasks(id);

CREATE INDEX ix_tasks_is_recurring ON tasks(is_recurring);
CREATE INDEX ix_tasks_parent_task_id ON tasks(parent_task_id);
```

### Migration 004: Create push_subscriptions table

```sql
CREATE TABLE push_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    endpoint TEXT NOT NULL,
    p256dh_key TEXT NOT NULL,
    auth_key TEXT NOT NULL,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, endpoint)
);

CREATE INDEX ix_push_subscriptions_user_id ON push_subscriptions(user_id);
```

---

## Validation Rules (Extended)

| Entity | Field | Rule |
|--------|-------|------|
| Task | recurrence_rule | One of: "daily", "weekly", "monthly", "weekdays", or "cron:*" |
| Task | recurrence_end | Must be after created_at if set |
| Task | parent_task_id | Must reference existing task if set |
| Task | reminder_at | Must be in future when setting (not when processing) |
| PushSubscription | endpoint | Valid HTTPS URL |
| PushSubscription | p256dh_key | Base64-encoded string |
| ReminderEvent | task_id | Must exist and not be deleted |
| TaskEvent | event_type | One of: created, updated, completed, deleted |
