# Implementation Plan: Cloud Deployment to DigitalOcean

**Branch**: `005-cloud-deployment` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-cloud-deployment/spec.md`

## Summary

Deploy the existing Phase 4 Todo Chatbot application to DigitalOcean Kubernetes (DOKS) with budget-optimized configuration ($24/month target). Uses existing Helm charts with DOKS-specific values, NodePort for cost savings, and GitHub Actions for CI/CD automation.

## Technical Context

**Language/Version**: YAML (Helm/K8s), Bash (scripts), YAML (GitHub Actions)
**Primary Dependencies**: Helm 3.x, kubectl, doctl CLI, Docker
**Storage**: Existing Neon PostgreSQL (external, no changes)
**Testing**: Manual verification (kubectl commands, browser access)
**Target Platform**: DigitalOcean Kubernetes (DOKS) - nyc1 region
**Project Type**: Infrastructure/DevOps (deployment configuration only)
**Performance Goals**: Application accessible within 10 minutes of deployment
**Constraints**: <$30/month budget, single node (4GB RAM), no LoadBalancer
**Scale/Scope**: 1 node cluster, 1 replica per service, development/demo use

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Specification created before implementation |
| II. Clean Code | PASS | Infrastructure code follows YAML best practices |
| III. Test-First Development | N/A | Infrastructure deployment - manual verification |
| IV. Single Responsibility | PASS | Separate files for each concern (values, workflow, script) |
| V. Evolutionary Architecture | PASS | Extends Phase 4 without code changes |
| VI. User Experience First | PASS | Clear access URL, automated deployment |

**Gate Result**: PASS - No violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/005-cloud-deployment/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (minimal - infrastructure focus)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── deployment.yaml  # Deployment contract specification
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
phase-5-cloud/
├── backend/                    # Existing (no changes)
├── frontend/                   # Existing (no changes)
├── helm/
│   └── todo-app/
│       ├── Chart.yaml          # Existing
│       ├── values.yaml         # Existing (default)
│       ├── values-dev.yaml     # Existing (development)
│       └── values-doks.yaml    # NEW - DigitalOcean config
├── scripts/
│   └── doks/
│       └── deploy.sh           # NEW - Manual deploy script
├── docker-compose.yml          # Existing
└── README.md                   # Update with DOKS instructions

.github/
└── workflows/
    └── deploy-doks.yml         # NEW - CI/CD workflow
```

**Structure Decision**: Extends existing Phase 4 structure with DOKS-specific configuration files. No changes to application code - only deployment configuration.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DigitalOcean Cloud                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              DOKS Cluster (1 node, s-2vcpu-4gb)           │  │
│  │  ┌─────────────────┐    ┌─────────────────┐              │  │
│  │  │    Frontend     │    │    Backend      │              │  │
│  │  │   (NodePort     │───▶│   (ClusterIP    │              │  │
│  │  │    :30080)      │    │    :8000)       │              │  │
│  │  └─────────────────┘    └────────┬────────┘              │  │
│  └──────────────────────────────────┼────────────────────────┘  │
│                                     │                            │
│  ┌─────────────────┐               │                            │
│  │ Container       │               │                            │
│  │ Registry (Free) │               │                            │
│  └─────────────────┘               │                            │
└─────────────────────────────────────┼────────────────────────────┘
                                      │
                                      ▼
                          ┌─────────────────────┐
                          │  Neon PostgreSQL    │
                          │  (External)         │
                          └─────────────────────┘
```

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Service Type | NodePort | Saves $12/month vs LoadBalancer |
| Node Size | s-2vcpu-4gb | Minimum viable for frontend + backend + chatbot |
| Node Count | 1 | Budget constraint - no HA needed for demo |
| Registry | DO Free Tier | 500MB sufficient for 2 images |
| CI/CD | GitHub Actions | Free for public repos, integrated |

## Files to Create

| File | Purpose |
|------|---------|
| `phase-5-cloud/helm/todo-app/values-doks.yaml` | DOKS-specific Helm values |
| `phase-5-cloud/scripts/doks/deploy.sh` | Manual deployment script |
| `.github/workflows/deploy-doks.yml` | CI/CD workflow |

## Complexity Tracking

> No violations - infrastructure deployment extends existing patterns without complexity additions.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

---

## Part B: Advanced Features Implementation Plan

This section covers the implementation of reminders, notifications, and recurring tasks using event-driven architecture with Kafka and Dapr.

---

## Technical Context (Advanced Features)

**Language/Version**: Python 3.13+ (backend), TypeScript (frontend)
**Primary Dependencies**: Dapr SDK, aiokafka (via Dapr), pywebpush
**Storage**: Neon PostgreSQL (extended schema), Redpanda Cloud (Kafka)
**Testing**: pytest (unit), manual verification (integration)
**Target Platform**: DigitalOcean Kubernetes (DOKS) with Dapr
**Performance Goals**: Reminders delivered within 2 minutes of scheduled time
**Constraints**: Single node cluster, free tier Redpanda, browser notifications only
**Scale/Scope**: Hundreds of tasks per user, minutes-level reminder precision

---

## Architecture Overview (Advanced Features)

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                              DIGITALOCEAN KUBERNETES (DOKS)                           │
│                                                                                       │
│  ┌─────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐  │
│  │   Frontend Pod      │   │    Backend Pod          │   │  Notification Pod       │  │
│  │  ┌───────┐ ┌──────┐ │   │  ┌───────┐ ┌───────┐   │   │  ┌───────┐ ┌───────┐   │  │
│  │  │Next.js│ │ Dapr │ │   │  │FastAPI│ │ Dapr  │   │   │  │Worker │ │ Dapr  │   │  │
│  │  │  App  │◀┼▶Sidecar│ │   │  │+ MCP  │◀┼▶Sidecar│   │   │  │Service│◀┼▶Sidecar│   │  │
│  │  └───────┘ └──────┘ │   │  └───┬───┘ └───────┘   │   │  └───┬───┘ └───────┘   │  │
│  └─────────────────────┘   └──────┼─────────────────┘   └──────┼─────────────────┘  │
│                                   │                            │                    │
│                           ┌───────▼────────────────────────────▼───────┐            │
│                           │              DAPR COMPONENTS               │            │
│                           │  ┌────────────────┐  ┌────────────────┐   │            │
│                           │  │ pubsub.kafka   │  │ bindings.cron  │   │            │
│                           │  │ (Redpanda)     │  │ (*/1 * * * *)  │   │            │
│                           │  └───────┬────────┘  └───────┬────────┘   │            │
│                           │          │                   │            │            │
│                           │  ┌───────▼───────────────────▼────────┐   │            │
│                           │  │     secretstores.kubernetes        │   │            │
│                           │  └────────────────────────────────────┘   │            │
│                           └───────────────────────────────────────────┘            │
│                                          │                                          │
└──────────────────────────────────────────┼──────────────────────────────────────────┘
                                           │
                           ┌───────────────▼───────────────┐
                           │      EXTERNAL SERVICES        │
                           │  ┌─────────────────────────┐  │
                           │  │   Redpanda Cloud        │  │
                           │  │   (Kafka - Free Tier)   │  │
                           │  │   Topics:               │  │
                           │  │   - task-events         │  │
                           │  │   - reminders           │  │
                           │  │   - task-updates        │  │
                           │  └─────────────────────────┘  │
                           │  ┌─────────────────────────┐  │
                           │  │   Neon PostgreSQL       │  │
                           │  │   (Extended Schema)     │  │
                           │  └─────────────────────────┘  │
                           └───────────────────────────────┘
```

---

## Key Design Decisions (Advanced Features)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event Streaming | Redpanda Cloud | Free tier, Kafka-compatible, no Zookeeper |
| Runtime | Dapr | Abstracts infrastructure, enables cron binding |
| Notification | Browser Push | Free, no external services needed |
| Reminder Check | 1-minute cron | Balance between precision and resource usage |
| Recurring Pattern | Event-driven | Decoupled, reliable, handles service restarts |
| Service Architecture | Separate notification service | Independent scaling, failure isolation |

---

## Project Structure (Extended)

```text
phase-5-cloud/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── task.py              # MODIFY - add new fields
│   │   │   └── push_subscription.py # NEW - browser push subscriptions
│   │   ├── schemas/
│   │   │   ├── task.py              # MODIFY - add new fields to schemas
│   │   │   └── events.py            # NEW - Kafka event schemas
│   │   ├── routers/
│   │   │   ├── tasks.py             # MODIFY - publish events on CRUD
│   │   │   ├── internal.py          # NEW - internal endpoints for reminders
│   │   │   └── subscriptions.py     # NEW - push subscription endpoints
│   │   ├── services/
│   │   │   ├── event_publisher.py   # NEW - Dapr pub/sub wrapper
│   │   │   ├── recurrence.py        # NEW - recurrence calculation logic
│   │   │   └── recurring_handler.py # NEW - Kafka consumer for recurring tasks
│   │   └── main.py                  # MODIFY - add event routes
│   └── tests/
│       ├── test_reminders.py        # NEW
│       └── test_recurrence.py       # NEW
│
├── notification-service/            # NEW - separate microservice
│   ├── src/
│   │   ├── main.py                  # FastAPI app
│   │   ├── handlers.py              # Event handlers
│   │   └── push.py                  # Web push sender
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── CLAUDE.md
│
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   └── push-notifications.ts # NEW - push subscription logic
│   │   ├── app/
│   │   │   └── api/
│   │   │       └── push/
│   │   │           └── route.ts     # NEW - subscription endpoint
│   │   └── components/
│   │       └── reminder-picker.tsx  # NEW - UI for setting reminders
│   └── public/
│       └── sw.js                    # NEW - service worker
│
├── helm/
│   └── todo-app/
│       ├── values.yaml              # MODIFY - add notification service
│       ├── values-doks.yaml         # MODIFY - add Dapr & Kafka config
│       ├── templates/
│       │   ├── notification/        # NEW - notification service manifests
│       │   │   ├── deployment.yaml
│       │   │   └── service.yaml
│       │   └── dapr/                # NEW - Dapr component manifests
│       │       ├── pubsub.yaml
│       │       ├── cron-binding.yaml
│       │       └── secrets.yaml
│       └── Chart.yaml               # MODIFY - bump version
│
├── scripts/
│   └── doks/
│       ├── deploy.sh                # MODIFY - add Dapr init
│       └── setup-redpanda.sh        # NEW - Redpanda setup helper
│
└── docker-compose.yml               # MODIFY - add notification service
```

---

## Files to Create (Advanced Features)

| File | Purpose |
|------|---------|
| `backend/src/models/push_subscription.py` | SQLModel for browser push subscriptions |
| `backend/src/schemas/events.py` | Pydantic schemas for Kafka events |
| `backend/src/routers/internal.py` | Internal endpoints for cron triggers |
| `backend/src/routers/subscriptions.py` | Push subscription CRUD |
| `backend/src/services/event_publisher.py` | Dapr pub/sub wrapper |
| `backend/src/services/recurrence.py` | Next occurrence calculation |
| `backend/src/services/recurring_handler.py` | Kafka consumer for task-events |
| `notification-service/` | Entire new microservice |
| `frontend/src/lib/push-notifications.ts` | Browser push registration |
| `frontend/public/sw.js` | Service worker for notifications |
| `helm/todo-app/templates/notification/` | K8s manifests for notification service |
| `helm/todo-app/templates/dapr/` | Dapr component configurations |

---

## Files to Modify (Advanced Features)

| File | Changes |
|------|---------|
| `backend/src/models/task.py` | Add reminder_sent, due_at, is_recurring, recurrence_rule, recurrence_end, parent_task_id |
| `backend/src/schemas/task.py` | Add new fields to request/response schemas |
| `backend/src/routers/tasks.py` | Publish events on create/update/complete/delete |
| `backend/src/main.py` | Register new routers, add event handlers |
| `helm/todo-app/values.yaml` | Add notification service config |
| `helm/todo-app/values-doks.yaml` | Add Dapr annotations, Kafka secrets |
| `helm/todo-app/Chart.yaml` | Bump version to 2.0.0 |

---

## Implementation Phases

### Phase A: Database Schema Extension
1. Add new fields to Task model
2. Create PushSubscription model
3. Run migrations on Neon database
4. Update Pydantic schemas

### Phase B: Dapr Infrastructure
1. Install Dapr on DOKS cluster
2. Create Redpanda Cloud account and topics
3. Configure Dapr pub/sub component
4. Configure Dapr cron binding
5. Test pub/sub with simple messages

### Phase C: Backend Event Publishing
1. Create event publisher service
2. Modify task CRUD to publish events
3. Create internal endpoints for cron triggers
4. Add due reminder query endpoint
5. Test event flow

### Phase D: Notification Service
1. Create notification-service microservice
2. Implement Kafka consumer for reminders topic
3. Implement Web Push sender
4. Create Dockerfile and Helm templates
5. Deploy to DOKS

### Phase E: Frontend Push Integration
1. Create Service Worker for notifications
2. Implement push subscription registration
3. Add reminder picker UI component
4. Connect to backend subscription API
5. Test end-to-end notification flow

### Phase F: Recurring Tasks
1. Implement recurrence calculation logic
2. Add Kafka consumer for task-events
3. Create next occurrence on completion
4. Add chatbot commands for recurring tasks
5. Test recurring task lifecycle

---

## Complexity Tracking (Advanced Features)

| Addition | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|-------------------------------------|
| Notification Service | Separation of concerns, independent scaling | Inline processing would block main backend |
| Dapr | Abstracts Kafka, provides cron binding | Direct Kafka client requires more boilerplate |
| Kafka/Redpanda | Reliable event delivery, at-least-once | In-memory queues lose events on restart |
| Browser Push | Free, works offline | Email/SMS have cost and complexity |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Redpanda free tier limits | Monitor usage, upgrade if needed |
| Browser push blocked | Graceful degradation, show in-app badge |
| Dapr learning curve | Use simple HTTP API, avoid complex features |
| Single node overload | Conservative resource limits, scale up if needed |

---

## Dependencies Between User Stories

```
US1 (Basic Deploy) ──────────────────────────────────┐
                                                      │
US2 (CI/CD) ─────────────────────────────────────────┤
                                                      │
US3 (Cost) ──────────────────────────────────────────┤
                                                      ▼
                                              ┌───────────────┐
                                              │   US6 (Kafka/ │
                                              │   Event Arch) │
                                              └───────┬───────┘
                                                      │
                              ┌────────────────┬──────┴──────┐
                              ▼                ▼             ▼
                        ┌──────────┐    ┌──────────┐   ┌──────────┐
                        │ US7 Dapr │    │US4 Remind│   │US5 Recur │
                        └──────────┘    └──────────┘   └──────────┘
```

**Key Dependencies**:
- US4, US5, US6, US7 all require US1 (basic deployment) to be complete
- US4 (Reminders) requires US6 (Kafka) and US7 (Dapr) infrastructure
- US5 (Recurring) requires US6 (Kafka) for event-driven recreation
- US7 (Dapr) is foundational for US4 and US5
