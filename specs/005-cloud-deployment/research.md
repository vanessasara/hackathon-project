# Research: Cloud Deployment to DigitalOcean

**Feature**: 005-cloud-deployment
**Date**: 2025-12-04

## Research Summary

This document captures research findings for deploying Phase 4 Todo Chatbot to DigitalOcean Kubernetes (DOKS) with budget optimization.

---

## R1: DigitalOcean Kubernetes (DOKS) Pricing

**Question**: What is the most cost-effective DOKS configuration?

**Decision**: Single node cluster with `s-2vcpu-4gb` droplet

**Rationale**:
- `s-1vcpu-2gb` ($12/month) has only 2GB RAM - insufficient for Next.js + FastAPI + AI services
- `s-2vcpu-4gb` ($24/month) provides 4GB RAM - minimum viable for all services
- Single node eliminates control plane complexity and reduces costs
- No high availability needed for demo/development use

**Alternatives Considered**:
| Option | Cost | RAM | Verdict |
|--------|------|-----|---------|
| s-1vcpu-2gb x1 | $12/mo | 2GB | Too small - OOM risk |
| s-2vcpu-4gb x1 | $24/mo | 4GB | **Selected** |
| s-2vcpu-4gb x2 | $48/mo | 8GB | Over budget |

---

## R2: Service Exposure Strategy

**Question**: How to expose the application to the internet cost-effectively?

**Decision**: NodePort on port 30080

**Rationale**:
- LoadBalancer costs $12/month additional
- NodePort is free - directly exposes service on node's external IP
- Port 30080 is in valid NodePort range (30000-32767)
- Acceptable UX for demo: `http://<NODE_IP>:30080`

**Alternatives Considered**:
| Option | Cost | UX | Verdict |
|--------|------|-------|---------|
| LoadBalancer | +$12/mo | Clean URL | Over budget |
| NodePort | Free | IP:Port URL | **Selected** |
| Ingress + LB | +$12/mo+ | Domain support | Over budget |

---

## R3: Container Registry

**Question**: Where to store Docker images?

**Decision**: DigitalOcean Container Registry (Free Tier)

**Rationale**:
- Free tier provides 500MB storage
- Frontend image: ~200MB, Backend image: ~150MB
- Total: ~350MB - fits within free tier
- Integrated with DOKS - simple authentication

**Alternatives Considered**:
| Option | Cost | Limit | Verdict |
|--------|------|-------|---------|
| DO Registry Free | Free | 500MB | **Selected** |
| DO Registry Basic | $5/mo | 5GB | Unnecessary |
| Docker Hub Free | Free | 1 private | Auth complexity |
| GitHub Container Registry | Free | Unlimited public | Extra config |

---

## R4: CI/CD Platform

**Question**: How to automate deployments?

**Decision**: GitHub Actions

**Rationale**:
- Free for public repositories
- Native integration with GitHub
- `digitalocean/action-doctl` official action available
- Simple workflow syntax

**Workflow Triggers**:
- Push to `main` branch triggers deployment
- Manual trigger via `workflow_dispatch` for debugging

---

## R5: Resource Limits

**Question**: How to configure resource limits for single 4GB node?

**Decision**: Conservative limits with room for system overhead

**Rationale**:
- Node has 4GB total, ~3.5GB allocatable after system reservations
- Frontend: 128Mi request, 256Mi limit
- Backend: 128Mi request, 256Mi limit
- Total requests: 256Mi (leaves 3.2GB headroom)
- Total limits: 512Mi (allows bursting)

**Resource Allocation**:
```yaml
Frontend:
  requests: { memory: "128Mi", cpu: "50m" }
  limits: { memory: "256Mi", cpu: "200m" }
Backend:
  requests: { memory: "128Mi", cpu: "50m" }
  limits: { memory: "256Mi", cpu: "200m" }
```

---

## R6: Secrets Management

**Question**: How to securely manage secrets in CI/CD?

**Decision**: GitHub Secrets + Kubernetes Secrets

**Rationale**:
- GitHub Secrets store sensitive values encrypted
- CI/CD passes secrets to Helm via `--set`
- Helm creates Kubernetes Secret resource
- Pods mount secrets as environment variables

**Required Secrets**:
| GitHub Secret | Purpose |
|---------------|---------|
| DIGITALOCEAN_ACCESS_TOKEN | DOKS API access |
| DATABASE_URL | Neon PostgreSQL connection |
| BETTER_AUTH_SECRET | JWT signing key |
| OPENAI_API_KEY | AI chatbot functionality |

---

---

## Part B: Advanced Features Research

Research findings for implementing reminders, notifications, and recurring tasks with event-driven architecture.

---

## R7: Event Streaming Platform Selection

**Question**: Which Kafka-compatible platform is best for budget-constrained deployment?

**Decision**: Redpanda Cloud (Serverless Free Tier)

**Rationale**:
- Free serverless tier with no credit card required for basic usage
- Kafka-compatible API - existing Kafka libraries work unchanged
- No Zookeeper dependency - simpler architecture
- Fast setup (under 5 minutes)
- REST API + Native Kafka protocol support

**Alternatives Considered**:
| Option | Cost | Pros | Cons | Verdict |
|--------|------|------|------|---------|
| Redpanda Cloud | Free tier | Kafka-compatible, no Zookeeper | Newer ecosystem | **Selected** |
| Confluent Cloud | $400 credit/30 days | Industry standard | Credit expires | Trial only |
| CloudKarafka | Free "Duck" plan | Simple | 5 topics, limited throughput | Too limited |
| Strimzi (self-hosted) | Free (compute cost) | Full control | Complex setup | Backup option |

**Implementation Notes**:
- Sign up at redpanda.com/cloud
- Create serverless cluster (free tier)
- Create topics: `task-events`, `reminders`, `task-updates`
- Use SASL/SCRAM authentication

---

## R8: Distributed Application Runtime (Dapr)

**Question**: How to abstract infrastructure concerns (pub/sub, cron, secrets) for portability?

**Decision**: Dapr (Distributed Application Runtime)

**Rationale**:
- Runs as sidecar - no library dependencies in application code
- Pub/Sub abstraction - switch Kafka to RabbitMQ with config change only
- Built-in cron binding for scheduled jobs (reminder checks)
- Secrets management integration with Kubernetes
- Service-to-service invocation with automatic retries
- Free and open source

**Dapr Building Blocks Used**:
| Building Block | Use Case | Component Type |
|----------------|----------|----------------|
| Pub/Sub | Task events to Kafka | `pubsub.kafka` |
| Bindings | Cron trigger for reminders | `bindings.cron` |
| Secrets | Kafka credentials, API keys | `secretstores.kubernetes` |
| Service Invocation | Frontend → Backend calls | Built-in |

**Installation on Kubernetes**:
```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr on cluster
dapr init -k --wait

# Verify installation
kubectl get pods -n dapr-system
```

---

## R9: Reminder Architecture Pattern

**Question**: How to implement reliable task reminders at scale?

**Decision**: Cron-based polling with event-driven notification delivery

**Rationale**:
- Dapr cron binding triggers `/check-reminders` endpoint every minute
- Endpoint queries tasks with `reminder_at <= now AND reminder_sent = false`
- For each due task, publish event to Kafka `reminders` topic
- Notification service consumes events and sends browser notifications
- Mark `reminder_sent = true` after successful delivery

**Why not per-task timers?**
- Kubernetes doesn't support millions of fine-grained timers
- Database polling every minute is simple and reliable
- Kafka ensures at-least-once delivery if notification service is down

**Reminder Flow**:
```
[Dapr Cron: */1 * * * *]
        │
        ▼
[Backend: GET /check-reminders]
        │
        ▼
[Query: reminder_at <= now AND NOT reminder_sent]
        │
        ▼
[Publish to Kafka: reminders topic]
        │
        ▼
[Notification Service: consume & send]
        │
        ▼
[Backend: PATCH /tasks/{id}/reminder-sent]
```

---

## R10: Recurring Task Pattern

**Question**: How to implement recurring task auto-recreation?

**Decision**: Event-driven recreation on task completion

**Rationale**:
- When recurring task is completed, publish `TaskCompletedEvent` to Kafka
- Recurring task service consumes event and calculates next occurrence
- New task created with same title, updated due date, link to parent task
- Supports patterns: `daily`, `weekly`, `monthly`, `weekdays`, custom cron

**Recurrence Rule Format**:
| Pattern | Example | Next After |
|---------|---------|------------|
| `daily` | Every day | +1 day |
| `weekly` | Every week | +7 days |
| `monthly` | Every month | +1 month |
| `weekdays` | Mon-Fri | Next weekday |
| `cron:0 9 * * 1` | Mon 9am | Next matching |

**Database Fields**:
```python
is_recurring: bool           # True if this is a recurring task
recurrence_rule: str         # "daily", "weekly", "monthly", "cron:..."
recurrence_end: datetime     # Optional end date
parent_task_id: int          # Link to original task (for occurrences)
```

---

## R11: Notification Delivery Method

**Question**: How to deliver notifications to users?

**Decision**: Browser Push Notifications (Phase 1), extensible to email/SMS

**Rationale**:
- Browser notifications work without external services (no cost)
- Service Worker can receive notifications even when tab is closed
- Web Push API is standardized across browsers
- Can extend to email (SendGrid free tier) or SMS (Twilio) later

**Implementation**:
1. Frontend registers Service Worker on login
2. Obtains push subscription (endpoint + keys)
3. Stores subscription in database (new `push_subscriptions` table)
4. Notification service sends via Web Push protocol

**Alternatives for Future**:
| Method | Cost | Pros | Cons |
|--------|------|------|------|
| Browser Push | Free | No dependencies | Requires browser open |
| Email (SendGrid) | Free 100/day | Reliable | Slower delivery |
| SMS (Twilio) | ~$0.01/msg | Most reliable | Cost at scale |

---

## R12: Kafka Topics Design

**Question**: What Kafka topics are needed and what events flow through them?

**Decision**: Three topics with specific purposes

**Topics**:
| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `task-events` | Backend | Recurring Service, Audit | All task CRUD events |
| `reminders` | Backend (cron) | Notification Service | Due reminder triggers |
| `task-updates` | Backend | WebSocket Service (future) | Real-time sync |

**Event Schemas**:

```json
// task-events topic
{
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "user_id": "user_abc",
  "task_data": { "title": "...", "is_recurring": true, ... },
  "timestamp": "2025-12-08T10:30:00Z"
}

// reminders topic
{
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Morning standup",
  "reminder_at": "2025-12-08T09:00:00Z",
  "push_subscription": { "endpoint": "...", "keys": {...} }
}
```

---

## R13: Resource Requirements (Advanced Features)

**Question**: Can advanced features fit on single 4GB node?

**Decision**: Yes, with optimized resource allocation

**Updated Resource Budget**:
| Service | Memory Request | Memory Limit | CPU Request |
|---------|---------------|--------------|-------------|
| Frontend | 128Mi | 256Mi | 50m |
| Backend | 128Mi | 256Mi | 50m |
| Notification | 64Mi | 128Mi | 25m |
| Dapr Sidecar (x3) | 64Mi each | 128Mi each | 25m each |
| **Total** | **512Mi** | **1GB** | **225m** |

**Remaining on 4GB node**: ~2.5GB headroom for system and bursting

**Conclusion**: Single node remains viable for development/demo with advanced features.

---

## Unresolved Items

None - all research questions resolved.

## References

- [DigitalOcean Kubernetes Pricing](https://www.digitalocean.com/pricing/kubernetes)
- [DigitalOcean Container Registry](https://docs.digitalocean.com/products/container-registry/)
- [Kubernetes NodePort Services](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)
- [GitHub Actions for DigitalOcean](https://github.com/digitalocean/action-doctl)

### References (Advanced Features)

- [Redpanda Cloud](https://redpanda.com/cloud) - Kafka-compatible streaming
- [Dapr Documentation](https://docs.dapr.io/) - Distributed application runtime
- [Dapr Pub/Sub](https://docs.dapr.io/developing-applications/building-blocks/pubsub/) - Event-driven messaging
- [Dapr Cron Binding](https://docs.dapr.io/reference/components-reference/supported-bindings/cron/) - Scheduled triggers
- [Web Push Protocol](https://web.dev/push-notifications-overview/) - Browser notifications
- [Kafka Python Client](https://kafka-python.readthedocs.io/) - Python Kafka library
