# Feature Specification: Cloud Deployment to DigitalOcean

**Feature Branch**: `005-cloud-deployment`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Deploy Phase 4 Todo Chatbot to DigitalOcean Kubernetes with budget-optimized configuration and GitHub Actions CI/CD"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Application from Internet (Priority: P1)

As a user, I want to access the Todo Chatbot application from anywhere on the internet so that I can manage my tasks and interact with the AI assistant without running it locally.

**Why this priority**: This is the core value proposition - making the application publicly accessible is the fundamental goal of cloud deployment.

**Independent Test**: Can be fully tested by navigating to the public IP address in a browser and verifying the application loads and is functional.

**Acceptance Scenarios**:

1. **Given** the application is deployed to DOKS, **When** I navigate to http://<NODE_IP>:30080 in a browser, **Then** I see the Todo Chatbot login page
2. **Given** I have valid credentials, **When** I log in to the deployed application, **Then** I can access my todos and the AI chatbot
3. **Given** the application is deployed, **When** I create a new task via the web interface, **Then** the task is persisted and visible on refresh

---

### User Story 2 - Automated Deployment via CI/CD (Priority: P2)

As a developer, I want code changes pushed to the main branch to automatically deploy to the cloud so that I can release updates without manual intervention.

**Why this priority**: Automated deployments reduce manual work and human error, enabling faster iteration cycles.

**Independent Test**: Can be tested by pushing a commit to main branch and verifying the new version is deployed within minutes.

**Acceptance Scenarios**:

1. **Given** code is pushed to the main branch, **When** the GitHub Actions workflow runs, **Then** new container images are built and pushed to the registry
2. **Given** new images are in the registry, **When** the deployment step runs, **Then** the Kubernetes cluster is updated with the new images
3. **Given** deployment completes, **When** I access the application, **Then** I see the updated version

---

### User Story 3 - Cost-Effective Operation (Priority: P3)

As an application owner, I want the cloud infrastructure to cost less than $30/month so that I can run the application affordably during development and demonstration phases.

**Why this priority**: Budget constraints are real - ensuring cost-effectiveness allows sustainable operation without financial burden.

**Independent Test**: Can be verified by checking the DigitalOcean billing dashboard after one month of operation.

**Acceptance Scenarios**:

1. **Given** the DOKS cluster is configured, **When** I review the DigitalOcean billing, **Then** monthly costs are under $30
2. **Given** NodePort is used instead of LoadBalancer, **When** I access the application, **Then** it remains accessible without the $12/month LoadBalancer cost
3. **Given** single replica configuration, **When** traffic is normal, **Then** the application performs acceptably for development/demo use

---

### Edge Cases

- What happens when the single node becomes unavailable? Application becomes inaccessible until node recovers (acceptable for budget tier - no HA)
- How does the system handle container registry quota exceeded? Build fails with clear error; user must clean up old images or upgrade registry tier
- What happens if GitHub Actions secrets are misconfigured? Deployment fails with authentication error; logs indicate which secret is missing
- How does the system handle Kubernetes resource exhaustion on single node? Pods may fail to schedule; monitoring via `kubectl get pods` shows pending status

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST deploy the Phase 4 application to DigitalOcean Kubernetes without code modifications
- **FR-002**: System MUST expose the frontend application via NodePort on port 30080
- **FR-003**: System MUST enable internal communication between frontend and backend services within the cluster
- **FR-004**: System MUST automatically build and push Docker images to DigitalOcean Container Registry on push to main branch
- **FR-005**: System MUST automatically deploy updated images to the Kubernetes cluster after successful build
- **FR-006**: System MUST securely manage secrets (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, DIGITALOCEAN_ACCESS_TOKEN) via Kubernetes secrets and GitHub secrets
- **FR-007**: System MUST provide a manual deployment script for local deployment without CI/CD

### Infrastructure Requirements

- **IR-001**: DOKS cluster MUST use single node configuration (s-2vcpu-4gb) for budget optimization
- **IR-002**: Container registry MUST use free tier (500MB limit)
- **IR-003**: Service type MUST be NodePort (not LoadBalancer) to avoid additional costs
- **IR-004**: Resource limits MUST be configured to fit within single 4GB RAM node

### Key Entities

- **DOKS Cluster**: DigitalOcean managed Kubernetes cluster hosting the application
- **Container Registry**: DigitalOcean container registry storing Docker images
- **Helm Chart**: Kubernetes deployment configuration with DOKS-specific values
- **GitHub Actions Workflow**: CI/CD pipeline configuration for automated deployment
- **Secrets**: Encrypted credentials for database, authentication, AI services, and cloud provider

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application is accessible via public IP within 10 minutes of initial deployment
- **SC-002**: Automated deployment completes within 10 minutes of pushing to main branch
- **SC-003**: Monthly infrastructure cost remains below $30 (target: $24)
- **SC-004**: Application performs acceptably with response times under 3 seconds for typical operations
- **SC-005**: Zero code changes required to Phase 4 application for cloud deployment
- **SC-006**: Deployment can be triggered both automatically (CI/CD) and manually (script)

---

## Part B: Advanced Features (Phase V-A from Hackathon)

The following user stories implement the Advanced Level features from the hackathon specification: Recurring Tasks, Due Dates & Time Reminders, and Event-Driven Architecture.

---

### User Story 4 - Task Reminders & Notifications (Priority: P4)

As a user, I want to set reminders on my tasks and receive notifications when they are due so that I never forget important deadlines.

**Why this priority**: Reminders are a core advanced feature that transforms the todo app from a simple list into a proactive assistant. Depends on basic deployment (US1) being functional.

**Independent Test**: Can be tested by creating a task with a reminder time 2 minutes in the future, then verifying a notification appears when the time arrives.

**Acceptance Scenarios**:

1. **Given** I create a task with a reminder set for a specific date/time, **When** that time arrives, **Then** I receive a browser notification with the task title
2. **Given** I have a task with a reminder, **When** I view my tasks via the chatbot ("show tasks with reminders"), **Then** the AI lists tasks with their reminder times
3. **Given** a reminder notification is sent, **When** I check the task, **Then** it shows the reminder was delivered (not sent repeatedly)
4. **Given** I update a task's reminder time via chatbot ("remind me about task 5 tomorrow at 9am"), **When** I view the task, **Then** the new reminder time is saved

---

### User Story 5 - Recurring Tasks / Reschedule (Priority: P5)

As a user, I want to create recurring tasks (daily, weekly, monthly) so that repetitive todos are automatically recreated when completed.

**Why this priority**: Recurring tasks build on the reminder system and require the event-driven architecture. This is the most complex advanced feature.

**Independent Test**: Can be tested by creating a daily recurring task, marking it complete, and verifying a new instance is automatically created for the next day.

**Acceptance Scenarios**:

1. **Given** I create a task with recurrence "daily" via chatbot ("add daily task: morning standup"), **When** I mark it complete, **Then** a new task is created for the next day with the same title
2. **Given** I have a weekly recurring task, **When** I ask the chatbot "reschedule my morning meetings to 2 PM", **Then** the recurrence pattern is updated for all future occurrences
3. **Given** I create a recurring task with an end date, **When** I complete the last occurrence, **Then** no new task is created after the end date
4. **Given** I have multiple recurring tasks, **When** I ask "show my recurring tasks", **Then** the chatbot lists all tasks with their recurrence patterns

---

### User Story 6 - Event-Driven Architecture (Priority: P4)

As a system operator, I want the application to use event-driven architecture with Kafka so that reminders and recurring tasks are processed reliably and the system scales horizontally.

**Why this priority**: This is the infrastructure foundation that enables US4 and US5. Must be implemented before or alongside reminders.

**Independent Test**: Can be tested by checking Kafka topic messages after task operations and verifying the notification service processes events.

**Acceptance Scenarios**:

1. **Given** a task with a due reminder is created, **When** the backend saves it, **Then** a reminder event is published to Kafka "reminders" topic
2. **Given** a recurring task is marked complete, **When** the completion is saved, **Then** a task-completed event is published to Kafka "task-events" topic
3. **Given** the notification service is running, **When** a reminder event arrives on Kafka, **Then** the service processes it and sends the notification
4. **Given** Dapr cron binding is configured, **When** the schedule triggers (every minute), **Then** due reminders are checked and events published

---

### User Story 7 - Dapr Integration (Priority: P4)

As a developer, I want to use Dapr for pub/sub, scheduled jobs, and service invocation so that infrastructure concerns are abstracted and the system is portable across environments.

**Why this priority**: Dapr simplifies Kafka integration and provides the cron binding needed for reminder scheduling. Enables cleaner code and easier local testing.

**Independent Test**: Can be tested by verifying Dapr sidecars are running and services can publish/subscribe to topics via Dapr HTTP API.

**Acceptance Scenarios**:

1. **Given** Dapr is installed on the cluster, **When** the backend publishes to "kafka-pubsub", **Then** messages appear in Redpanda/Kafka
2. **Given** Dapr cron binding is configured for 1-minute intervals, **When** 1 minute passes, **Then** the notification service receives a trigger at `/check-reminders`
3. **Given** services are annotated with Dapr sidecar, **When** frontend invokes backend via Dapr service invocation, **Then** the call succeeds with automatic retries
4. **Given** secrets are stored in Kubernetes secrets, **When** the app requests secrets via Dapr, **Then** credentials are returned without direct K8s API access

---

### Edge Cases (Advanced Features)

- What happens if the notification service is down when a reminder is due? Events remain in Kafka until consumed; reminders are eventually delivered (at-least-once semantics)
- What happens if a recurring task's recurrence rule is invalid? Task creation fails with validation error; user is prompted to correct the pattern
- How does the system handle timezone differences for reminders? All times stored in UTC; frontend converts to user's local timezone for display
- What happens if Kafka/Redpanda is unavailable? Backend continues to function for CRUD; events are queued locally or fail gracefully with error logged
- What happens if a user deletes a task while a reminder is pending? Notification service checks task existence before sending; deleted tasks are skipped

---

## Requirements - Advanced Features *(mandatory)*

### Functional Requirements (Advanced)

- **FR-100**: System MUST allow users to set reminder date/time on tasks via UI and chatbot
- **FR-101**: System MUST send browser notifications when task reminders are due
- **FR-102**: System MUST support recurring task patterns: daily, weekly, monthly
- **FR-103**: System MUST automatically create next occurrence when a recurring task is completed
- **FR-104**: System MUST allow users to set an end date for recurring tasks
- **FR-105**: System MUST publish task events to Kafka for async processing
- **FR-106**: System MUST process reminder events via a dedicated notification service
- **FR-107**: System MUST use Dapr for pub/sub abstraction and cron scheduling
- **FR-108**: System MUST check for due reminders at least every minute
- **FR-109**: System MUST mark reminders as sent to prevent duplicate notifications
- **FR-110**: System MUST support rescheduling tasks via natural language ("reschedule X to Y")

### Infrastructure Requirements (Advanced)

- **IR-100**: System MUST deploy Dapr sidecars alongside backend and notification services
- **IR-101**: System MUST use Redpanda Cloud (free tier) or self-hosted Kafka for event streaming
- **IR-102**: System MUST configure Dapr pub/sub component for Kafka connectivity
- **IR-103**: System MUST configure Dapr cron binding for reminder checks
- **IR-104**: Notification service MUST be a separate deployable microservice
- **IR-105**: Kafka credentials MUST be stored as Kubernetes secrets

### Key Entities (Advanced)

- **Task (extended)**: Add fields: `due_at`, `is_recurring`, `recurrence_rule`, `recurrence_end`, `parent_task_id`, `reminder_sent`
- **ReminderEvent**: Event published when reminder is due - contains task_id, user_id, title, due_at
- **TaskCompletedEvent**: Event published when recurring task is completed - triggers next occurrence creation
- **NotificationService**: Microservice that consumes Kafka events and sends notifications
- **DaprComponents**: Configuration for pub/sub (Kafka), cron binding, secrets store

---

## Success Criteria - Advanced Features *(mandatory)*

### Measurable Outcomes (Advanced)

- **SC-100**: Reminder notifications are delivered within 2 minutes of the scheduled time
- **SC-101**: Recurring task next occurrence is created within 5 seconds of completion
- **SC-102**: Event processing achieves at-least-once delivery (no lost events)
- **SC-103**: System handles 100 concurrent reminder events without degradation
- **SC-104**: Notification service processes events independently of main backend
- **SC-105**: Dapr abstracts Kafka - switching to RabbitMQ requires only config change, no code change
- **SC-106**: Natural language commands for reminders/recurring tasks have >90% intent recognition accuracy

---

## Assumptions

- User has or will create a DigitalOcean account
- Existing Neon PostgreSQL database remains accessible from DOKS cluster
- OpenAI API key has sufficient quota for AI chatbot functionality
- GitHub repository is accessible and user has permissions to configure secrets
- Single-node deployment without high availability is acceptable for this use case
- NodePort access (http://<IP>:30080) is acceptable without a custom domain
- 500MB container registry is sufficient for frontend and backend images

### Assumptions (Advanced Features)

- User will create a Redpanda Cloud account (free serverless tier) for Kafka
- Browser notifications are acceptable (no email/SMS notifications in initial implementation)
- UTC timezone storage is acceptable with frontend conversion
- Dapr free tier on Kubernetes is sufficient for the workload
- Notification service can share the same Neon database as the main backend
