# Tasks: Cloud Deployment to DigitalOcean

**Input**: Design documents from `/specs/005-cloud-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual verification only (infrastructure deployment - no automated tests)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Helm values**: `phase-5-cloud/helm/todo-app/`
- **Scripts**: `phase-5-cloud/scripts/doks/`
- **Workflows**: `.github/workflows/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify project structure and create directories for new files

- [x] T001 Verify phase-5-cloud directory exists with Phase 4 code copied
- [x] T002 [P] Create scripts/doks directory in phase-5-cloud/scripts/doks/
- [x] T003 [P] Create .github/workflows directory at repository root

---

## Phase 2: Foundational (Manual DigitalOcean Setup)

**Purpose**: Create DigitalOcean infrastructure - MUST complete before ANY deployment

**⚠️ CRITICAL**: These are MANUAL steps requiring DigitalOcean dashboard/CLI access

- [x] T004 Create DigitalOcean account at digitalocean.com
- [x] T005 Install doctl CLI (snap install doctl or brew install doctl)
- [x] T006 Authenticate doctl with API token (doctl auth init)
- [x] T007 Create DOKS cluster: `doctl kubernetes cluster create todo-app-cluster --region nyc1 --node-pool "name=default;size=s-2vcpu-4gb;count=1" --wait`
- [x] T008 Save kubeconfig: `doctl kubernetes cluster kubeconfig save todo-app-cluster`
- [x] T009 Create Container Registry: `doctl registry create todoappregistry2024` (unique name used)
- [x] T010 Connect registry to cluster: `doctl registry kubernetes-manifest | kubectl apply -f -`
- [ ] T011 Configure GitHub Secrets: DIGITALOCEAN_ACCESS_TOKEN, DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY

**Checkpoint**: DigitalOcean infrastructure ready - deployment configuration can now begin

---

## Phase 3: User Story 1 - Access Application from Internet (Priority: P1) 🎯 MVP

**Goal**: Deploy Phase 4 application to DOKS and make it accessible via public IP

**Independent Test**: Navigate to http://<NODE_IP>:30080 and verify login page loads

### Implementation for User Story 1

- [x] T012 [US1] Create values-doks.yaml with NodePort config in phase-5-cloud/helm/todo-app/values-doks.yaml
- [x] T013 [US1] Create manual deploy script in phase-5-cloud/scripts/doks/deploy.sh
- [x] T014 [US1] Make deploy.sh executable: chmod +x phase-5-cloud/scripts/doks/deploy.sh
- [x] T015 [US1] Login to DO registry: doctl registry login
- [x] T016 [US1] Build and push backend image: docker build -t registry.digitalocean.com/todoappregistry2024/backend:latest ./phase-5-cloud/backend && docker push registry.digitalocean.com/todoappregistry2024/backend:latest
- [x] T017 [US1] Build and push frontend image: docker build -t registry.digitalocean.com/todoappregistry2024/frontend:latest ./phase-5-cloud/frontend && docker push registry.digitalocean.com/todoappregistry2024/frontend:latest
- [x] T018 [US1] Deploy with Helm using values-doks.yaml
- [x] T019 [US1] Get Node IP: kubectl get nodes -o wide (206.81.11.248)
- [x] T020 [US1] Verify application loads at http://206.81.11.248:30080

**Checkpoint**: Application is accessible from the internet via NodePort - MVP complete

---

## Phase 4: User Story 2 - Automated Deployment via CI/CD (Priority: P2)

**Goal**: Create GitHub Actions workflow for automated deployment on push to main

**Independent Test**: Push commit to main branch and verify deployment completes automatically

### Implementation for User Story 2

- [x] T021 [US2] Create GitHub Actions workflow in .github/workflows/deploy-doks.yml
- [ ] T022 [US2] Verify GitHub Secrets are configured in repository settings
- [ ] T023 [US2] Test workflow by pushing to main branch
- [ ] T024 [US2] Monitor GitHub Actions for successful completion
- [ ] T025 [US2] Verify new deployment is live after workflow completes

**Checkpoint**: CI/CD pipeline is functional - code pushes automatically deploy

---

## Phase 5: User Story 3 - Cost-Effective Operation (Priority: P3)

**Goal**: Verify infrastructure costs are within budget (<$30/month)

**Independent Test**: Check DigitalOcean billing dashboard

### Implementation for User Story 3

- [ ] T026 [US3] Verify DOKS cluster uses single s-2vcpu-4gb node (~$24/month)
- [ ] T027 [US3] Verify Container Registry is on free tier (500MB)
- [ ] T028 [US3] Verify no LoadBalancer service (NodePort only)
- [ ] T029 [US3] Document final monthly cost estimate

**Checkpoint**: Cost verified at ~$24/month - within budget

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final cleanup

- [ ] T030 [P] Update phase-5-cloud/README.md with DOKS deployment instructions
- [ ] T031 [P] Add troubleshooting section to README
- [ ] T032 Verify all acceptance criteria from spec.md are met
- [ ] T033 Run quickstart.md validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 must complete before US2 (need manual deploy working first)
  - US3 can run in parallel with US2
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phase 2 (DO infrastructure)
- **User Story 2 (P2)**: Depends on US1 (need working deployment first)
- **User Story 3 (P3)**: Depends on Phase 2 (infrastructure exists to verify)

### Within Each User Story

- Configuration files before deployment commands
- Deployment before verification
- Manual verification at each checkpoint

### Parallel Opportunities

- T002 and T003 can run in parallel (different directories)
- T030 and T031 can run in parallel (different sections of README)
- US2 and US3 can run in parallel after US1 completes

---

## Parallel Example: Phase 1 Setup

```bash
# Launch setup tasks in parallel:
Task: "Create scripts/doks directory in phase-5-cloud/scripts/doks/"
Task: "Create .github/workflows directory at repository root"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (directories)
2. Complete Phase 2: Foundational (DO infrastructure - MANUAL)
3. Complete Phase 3: User Story 1 (manual deployment)
4. **STOP and VALIDATE**: Access app at http://<NODE_IP>:30080
5. Demo if ready - this is the MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Infrastructure ready
2. Add User Story 1 → Test manually → Demo (MVP!)
3. Add User Story 2 → Test CI/CD → Automated pipeline
4. Add User Story 3 → Verify costs → Budget confirmed
5. Each story adds value without breaking previous stories

---

## Task Summary

| Phase | Task Count | Purpose |
|-------|------------|---------|
| Phase 1: Setup | 3 | Directory structure |
| Phase 2: Foundational | 8 | DO infrastructure (manual) |
| Phase 3: US1 | 9 | Manual deployment (MVP) |
| Phase 4: US2 | 5 | CI/CD automation |
| Phase 5: US3 | 4 | Cost verification |
| Phase 6: Polish | 4 | Documentation |
| **Total** | **33** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Phase 2 tasks are MANUAL - require human interaction with DO dashboard/CLI
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

---

# Part B: Advanced Features Implementation

**Input**: Part B sections from spec.md, plan.md, data-model.md, research.md
**Prerequisites**: Part A deployment (US1-US3) must be functional

**Tests**: Mix of automated tests (backend logic) and manual verification (notifications, Kafka events)

---

## Phase 7: Event Infrastructure Setup (Shared for US4-US7)

**Purpose**: Set up Kafka (Redpanda) and Dapr infrastructure required by all advanced features

**⚠️ CRITICAL**: These are MANUAL steps requiring Redpanda Cloud and Kubernetes access

### Redpanda Cloud Setup (Manual)

- [x] T034 Create Redpanda Cloud account at redpanda.com/cloud (free serverless tier)
- [x] T035 Create serverless cluster in Redpanda Cloud dashboard (welcome cluster in ap-south-1)
- [x] T036 Create Kafka topics: `task-events`, `reminders`, `task-updates`
- [x] T037 Note bootstrap server URL and generate SASL credentials
- [ ] T038 Add GitHub Secrets: KAFKA_BOOTSTRAP_SERVERS, KAFKA_SASL_USERNAME, KAFKA_SASL_PASSWORD

### Dapr Installation on DOKS

- [ ] T039 Install Dapr CLI: `curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash`
- [ ] T040 Initialize Dapr on cluster: `dapr init -k --wait`
- [ ] T041 Verify Dapr installation: `kubectl get pods -n dapr-system`

### Dapr Components Configuration

- [x] T042 [P] Create Dapr Kafka pubsub component: phase-5-cloud/helm/todo-app/templates/dapr/kafka-pubsub.yaml
- [x] T043 [P] Create Dapr cron binding component: phase-5-cloud/helm/todo-app/templates/dapr/cron-binding.yaml
- [x] T044 [P] Create Kubernetes secret for Kafka credentials: phase-5-cloud/helm/todo-app/templates/dapr/kafka-secret.yaml
- [x] T045 Update values-doks.yaml with Kafka credentials placeholders

**Checkpoint**: Dapr and Kafka infrastructure ready - event-driven features can begin

---

## Phase 8: Database Schema Extension

**Purpose**: Add new fields to Task model and create PushSubscription table

### Database Migrations

- [x] T046 [US4] Add `reminder_sent` field to Task model: phase-5-cloud/backend/src/models/task.py
- [x] T047 [US4] Add `due_at` field to Task model
- [x] T048 [US5] Add recurring task fields: `is_recurring`, `recurrence_rule`, `recurrence_end`, `parent_task_id`
- [x] T049 [US4] Create PushSubscription model: phase-5-cloud/backend/src/models/push_subscription.py
- [x] T050 Update database.py to include new models (via models/__init__.py export)
- [x] T051 Run database migration against Neon PostgreSQL (migrate_part_b.py script)
- [x] T052 Verify new columns exist in database

**Checkpoint**: Database schema extended - backend can now use new fields

---

## Phase 9: User Story 4 - Task Reminders & Notifications (Priority: P4)

**Goal**: Enable users to set reminders and receive browser push notifications

**Independent Test**: Create task with reminder 2 minutes in future, verify notification appears

### Backend Reminder Implementation

- [x] T053 [US4] Update task schemas with reminder fields: phase-5-cloud/backend/src/schemas/task.py
- [x] T054 [US4] Update task router to handle reminder_at in create/update: phase-5-cloud/backend/src/routers/tasks.py
- [x] T055 [US4] Create Dapr client utility: phase-5-cloud/backend/src/dapr_client.py
- [x] T056 [US4] Create reminder check endpoint: GET /api/tasks/reminders/check in tasks router
- [x] T057 [US4] Implement query for due reminders: `reminder_at <= now AND NOT reminder_sent`
- [x] T058 [US4] Publish reminder events to Kafka via Dapr pubsub (in /reminders/binding endpoint)
- [x] T059 [US4] Add endpoint to mark reminder as sent: PATCH /api/tasks/{id}/reminder-sent

### Push Subscription Endpoints

- [x] T060 [US4] Create push subscription router: phase-5-cloud/backend/src/routers/push_subscriptions.py
- [x] T061 [US4] Add POST /api/push-subscriptions endpoint to save browser subscription
- [x] T062 [US4] Add DELETE /api/push-subscriptions endpoint to remove subscription
- [x] T063 [US4] Register push_subscriptions router in main.py

### Backend Tests

- [ ] T064 [US4] [P] Write tests for reminder check logic: phase-5-cloud/backend/tests/test_reminders.py
- [ ] T065 [US4] [P] Write tests for push subscription CRUD: phase-5-cloud/backend/tests/test_push_subscriptions.py

**Checkpoint**: Backend reminder API complete - notification service can consume events

---

## Phase 10: User Story 6 & 7 - Notification Service (Priority: P4)

**Goal**: Create separate microservice to consume Kafka events and send notifications

**Independent Test**: Publish test event to Kafka, verify notification service logs processing

### Notification Service Creation

- [x] T066 [US6] Create notification-service directory: phase-5-cloud/notification-service/
- [x] T067 [US6] Create pyproject.toml with dependencies: fastapi, dapr, pywebpush
- [x] T068 [US6] Create main.py with FastAPI app and Dapr subscription endpoint
- [x] T069 [US6] Create handlers.py with event processing logic
- [x] T070 [US6] Create push.py with Web Push notification sending (pywebpush)
- [x] T071 [US6] Generate VAPID keys for Web Push: phase-5-cloud/notification-service/generate_vapid.py
- [x] T072 [US6] Create Dockerfile for notification service
- [x] T073 [US6] Create CLAUDE.md documentation for notification service

### Dapr Subscription Configuration

- [x] T074 [US7] Create Dapr subscription for reminders topic (via /dapr/subscribe endpoint in main.py)
- [x] T075 [US7] Configure Dapr sidecar annotations in notification service deployment

### Helm Chart Updates for Notification Service

- [x] T076 [US6] Create notification service deployment template: phase-5-cloud/helm/todo-app/templates/notification/deployment.yaml
- [x] T077 [US6] Create notification service service template: phase-5-cloud/helm/todo-app/templates/notification/service.yaml
- [x] T078 [US6] Update values-doks.yaml with notification service config
- [x] T079 [US6] Add VAPID keys to Kubernetes secrets (in shared/secret.yaml)

### Notification Service Tests

- [ ] T080 [US6] [P] Write tests for event handlers: phase-5-cloud/notification-service/tests/test_handlers.py
- [ ] T081 [US6] [P] Write tests for push notification sending: phase-5-cloud/notification-service/tests/test_push.py

**Checkpoint**: Notification service deployed - can receive events and send notifications

---

## Phase 11: User Story 5 - Recurring Tasks (Priority: P5)

**Goal**: Implement recurring task patterns with automatic recreation on completion

**Independent Test**: Create daily recurring task, mark complete, verify new instance created for tomorrow

### Backend Recurring Task Logic

- [x] T082 [US5] Update task schemas with recurring fields: is_recurring, recurrence_rule, recurrence_end
- [x] T083 [US5] Create recurrence utility: phase-5-cloud/backend/src/utils/recurrence.py
- [x] T084 [US5] Implement next occurrence calculation for: daily, weekly, monthly, weekdays
- [x] T085 [US5] Implement cron expression parsing for custom patterns
- [x] T086 [US5] Update task completion logic to publish TaskCompletedEvent to Kafka
- [x] T087 [US5] Create recurring task handler in backend: integrated in toggle_task_complete endpoint
- [x] T088 [US5] Subscribe backend to task-events topic for recurring task processing
- [x] T089 [US5] Implement automatic task creation for next occurrence

### Recurring Task Tests

- [ ] T090 [US5] [P] Write tests for recurrence calculation: phase-5-cloud/backend/tests/test_recurrence.py
- [ ] T091 [US5] [P] Write tests for recurring task completion flow: phase-5-cloud/backend/tests/test_recurring_tasks.py

**Checkpoint**: Recurring tasks functional - completing triggers next occurrence creation

---

## Phase 12: Frontend Updates for Advanced Features

**Goal**: Add UI components for reminders, notifications, and recurring tasks

**Independent Test**: Set reminder via UI, verify notification permission requested and reminder saved

### Service Worker & Push Notifications

- [x] T092 [US4] Create Service Worker: phase-5-cloud/frontend/public/sw.js
- [x] T093 [US4] Implement push event handler in Service Worker
- [x] T094 [US4] Create notification permission request utility: phase-5-cloud/frontend/src/lib/notifications.ts
- [x] T095 [US4] Create push subscription registration utility
- [x] T096 [US4] Add VAPID public key to frontend environment (.env.local)

### Task Form Updates

- [x] T097 [US4] [P] Add reminder datetime picker to TaskForm component
- [x] T098 [US4] [P] Add due date picker to TaskForm component
- [x] T099 [US5] [P] Add recurring task toggle and pattern selector to TaskForm
- [x] T100 [US5] [P] Add recurrence end date picker (optional)

### Task Display Updates

- [x] T101 [US4] [P] Display reminder time on task cards (via indicator in TaskForm)
- [x] T102 [US4] [P] Display due date on task cards (via reminder indicator)
- [x] T103 [US5] [P] Display recurring indicator/badge on task cards (via indicator in TaskForm)
- [x] T104 [US5] [P] Display parent task link for recurring occurrences (data available via parent_task_id)

### AI Chatbot Integration

- [x] T105 [US4] Update AI agent tools to handle reminder setting: "remind me about X at Y"
- [x] T106 [US5] Update AI agent tools to handle recurring tasks: "add daily task X"
- [x] T107 [US5] Update AI agent tools to handle rescheduling: "reschedule X to Y"
- [x] T108 [US4] Add "show tasks with reminders" query support
- [x] T109 [US5] Add "show my recurring tasks" query support

**Checkpoint**: Frontend fully supports advanced features - end-to-end testing possible

---

## Phase 13: Integration Testing & Deployment

**Purpose**: Deploy advanced features and verify end-to-end functionality

### Build & Deploy

- [ ] T110 Build and push notification-service image to DO registry
- [ ] T111 Update GitHub Actions workflow to build notification-service
- [ ] T112 Deploy updated Helm chart with all advanced features
- [ ] T113 Verify Dapr sidecars are running for all services

### End-to-End Testing

- [ ] T114 [US4] Test: Create task with reminder, wait for notification
- [ ] T115 [US4] Test: Verify reminder_sent flag prevents duplicate notifications
- [ ] T116 [US5] Test: Create daily recurring task, complete, verify next occurrence
- [ ] T117 [US5] Test: Verify recurring task respects end date
- [ ] T118 [US6] Test: Verify Kafka events are published and consumed
- [ ] T119 [US7] Test: Verify Dapr cron triggers reminder checks every minute

### Performance Validation

- [ ] T120 Verify reminder delivery within 2 minutes of scheduled time
- [ ] T121 Verify recurring task creation within 5 seconds of completion
- [ ] T122 Verify system handles concurrent events without degradation

**Checkpoint**: All advanced features deployed and verified - production ready

---

## Phase 14: Polish & Documentation (Advanced Features)

**Purpose**: Documentation and cleanup for advanced features

- [ ] T123 [P] Update phase-5-cloud/README.md with advanced features documentation
- [ ] T124 [P] Update backend/CLAUDE.md with new endpoints and Dapr integration
- [ ] T125 [P] Update frontend documentation with notification setup
- [ ] T126 [P] Create notification-service/CLAUDE.md
- [ ] T127 Document Redpanda Cloud setup in deployment guide
- [ ] T128 Verify all acceptance criteria from spec.md Part B are met
- [ ] T129 Create ADR for event-driven architecture decisions

---

## Dependencies & Execution Order (Advanced Features)

### Phase Dependencies

- **Phase 7 (Event Infrastructure)**: Depends on Phase 3 completion (basic deployment working)
- **Phase 8 (Database Schema)**: Can run in parallel with Phase 7
- **Phase 9 (Reminders)**: Depends on Phase 7 + Phase 8
- **Phase 10 (Notification Service)**: Depends on Phase 7
- **Phase 11 (Recurring Tasks)**: Depends on Phase 8 + Phase 10
- **Phase 12 (Frontend)**: Depends on Phase 9 + Phase 11 (backend APIs ready)
- **Phase 13 (Integration)**: Depends on all previous phases
- **Phase 14 (Polish)**: Depends on Phase 13

### User Story Dependencies

```
US1 (Basic Deploy) ──┬──► US4 (Reminders) ──┬──► US5 (Recurring)
                     │                       │
                     └──► US6 (Events) ──────┤
                     │                       │
                     └──► US7 (Dapr) ────────┘
```

### Parallel Opportunities

- T042, T043, T044 (Dapr components) can run in parallel
- T046, T047, T048, T049 (database fields) can run in parallel
- T064, T065 (backend tests) can run in parallel
- T080, T081 (notification tests) can run in parallel
- T090, T091 (recurring tests) can run in parallel
- T097-T104 (frontend components) can run in parallel
- T123-T126 (documentation) can run in parallel

---

## Task Summary (Including Advanced Features)

| Phase | Task Range | Count | Purpose |
|-------|------------|-------|---------|
| Phase 1: Setup | T001-T003 | 3 | Directory structure |
| Phase 2: Foundational | T004-T011 | 8 | DO infrastructure (manual) |
| Phase 3: US1 | T012-T020 | 9 | Manual deployment (MVP) |
| Phase 4: US2 | T021-T025 | 5 | CI/CD automation |
| Phase 5: US3 | T026-T029 | 4 | Cost verification |
| Phase 6: Polish | T030-T033 | 4 | Documentation |
| **Part A Total** | T001-T033 | **33** | Basic Deployment |
| Phase 7: Event Infra | T034-T045 | 12 | Kafka + Dapr setup |
| Phase 8: DB Schema | T046-T052 | 7 | New fields + models |
| Phase 9: US4 Reminders | T053-T065 | 13 | Reminder backend |
| Phase 10: US6/7 Notification | T066-T081 | 16 | Notification service |
| Phase 11: US5 Recurring | T082-T091 | 10 | Recurring tasks |
| Phase 12: Frontend | T092-T109 | 18 | UI updates |
| Phase 13: Integration | T110-T122 | 13 | Deploy + test |
| Phase 14: Polish | T123-T129 | 7 | Documentation |
| **Part B Total** | T034-T129 | **96** | Advanced Features |
| **Grand Total** | T001-T129 | **129** | Complete Feature |

---

## Implementation Strategy (Advanced Features)

### Phase-by-Phase Approach

1. **Complete Part A first** (T001-T033) - Basic deployment must work
2. **Infrastructure setup** (Phase 7-8) - Kafka, Dapr, DB ready
3. **Backend features** (Phase 9-11) - APIs and logic
4. **Frontend features** (Phase 12) - UI components
5. **Integration & Polish** (Phase 13-14) - Testing and docs

### Risk Mitigation

1. **Redpanda Free Tier Limits**: Monitor usage; fall back to CloudKarafka if needed
2. **Dapr Complexity**: Test locally with Dapr first before DOKS deployment
3. **Browser Notification Permissions**: Graceful fallback if user denies permission
4. **Single Node Constraints**: Monitor resource usage; scale if OOM occurs

### Incremental Delivery

Each phase adds value:
- After Phase 8: Database ready for advanced features
- After Phase 9: Users can set reminders (no notifications yet)
- After Phase 10: Notifications work end-to-end
- After Phase 11: Recurring tasks functional
- After Phase 12: Full UI support
- After Phase 13: Production deployment verified
