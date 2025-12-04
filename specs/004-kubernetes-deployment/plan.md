# Implementation Plan: Local Kubernetes Deployment

**Branch**: `004-kubernetes-deployment` | **Date**: 2025-12-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-kubernetes-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy the Phase 3 Todo Chatbot application (Next.js 16 frontend + FastAPI backend with AI agents) to a local Minikube Kubernetes cluster using Helm charts. The deployment must include proper health checks, ConfigMap/Secret separation, NodePort service exposure, and comprehensive documentation for AI DevOps tools (kubectl-ai, kagent, Docker AI/Gordon). The primary goal is to create a production-ready deployment pattern that can scale to cloud Kubernetes platforms in future phases.

**Technical Approach**:
- Build Docker images in Minikube's Docker daemon (no external registry)
- Use monolithic Helm chart with modular templates (frontend, backend, shared)
- Expose frontend via NodePort 30300, keep backend internal (ClusterIP)
- Create automation scripts for one-command deployment
- Document AI-assisted operations with practical examples

## Technical Context

**Language/Version**:
- Backend: Python 3.13+ with FastAPI, SQLModel, OpenAI Agents SDK
- Frontend: TypeScript/Node.js 22+ with Next.js 16, React 19

**Primary Dependencies**:
- **Infrastructure**: Minikube 1.32+, Kubernetes 1.28+, Helm 3.x, Docker 24+
- **Backend**: FastAPI, SQLModel, Pydantic, OpenAI SDK, MCP SDK, uvicorn
- **Frontend**: Next.js 16, React 19, @openai/chatkit, Better Auth, Tailwind CSS
- **AI DevOps Tools**: kubectl-ai, kagent (Python packages), Docker AI (Gordon, built into Docker Desktop 4.53+)

**Storage**:
- **Database**: External Neon PostgreSQL (serverless, accessed via DATABASE_URL)
- **Object Storage**: External Cloudflare R2 (S3-compatible, accessed via R2 credentials)
- **Kubernetes**: No persistent volumes needed (stateless application)

**Testing**:
- **Backend**: pytest (existing Phase 3 tests)
- **Frontend**: Jest + React Testing Library (existing Phase 3 tests)
- **Deployment**: Shell scripts for verification (`verify.sh`, `test.sh`)
- **Health**: HTTP probes at `/api/health` endpoints

**Target Platform**:
- **Development**: Minikube on Linux/WSL2 with Docker driver
- **Cluster Config**: 4 CPUs, 8GB RAM, 20GB disk
- **Future**: Cloud Kubernetes (EKS, GKE, AKS) in Phase 5

**Project Type**: Web application (frontend + backend) + Kubernetes deployment

**Performance Goals**:
- Pods ready within 2 minutes of Helm install
- Frontend loads in <5 seconds after pod ready
- Health probe response time <1 second
- Image build time <5 minutes for both services

**Constraints**:
- Must use Minikube (not kind, k3s, or cloud)
- Must build images in Minikube Docker daemon (imagePullPolicy: Never)
- Must use Helm 3.x for deployment
- Must maintain Phase 3 code compatibility (no breaking changes)
- Must connect to external Neon DB and Cloudflare R2 (not in-cluster)
- Must document AI DevOps tools (kubectl-ai, kagent, Docker AI)

**Scale/Scope**:
- 2 services (frontend, backend)
- 2 deployments (1 replica each in dev)
- 2 services (NodePort, ClusterIP)
- 1 ConfigMap, 1 Secret
- ~10 Helm templates
- ~20 automation/documentation files
- 5+ AI DevOps tool examples

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-Driven Development ✅ PASS

- **Requirement**: All code MUST be generated from specifications using Claude Code
- **Status**: Specification created in `/sp.specify` command
- **Compliance**: Helm charts, scripts, and configuration will be generated from this plan
- **Note**: This is infrastructure code, not application code - Claude Code will generate all Kubernetes manifests

### II. Clean Code ✅ PASS

- **Requirement**: Code MUST follow conventions and maintain high readability
- **Status**: Will apply to Shell scripts and Helm templates
- **Compliance**:
  - Helm templates will use clear naming (frontend-deployment.yaml, backend-service.yaml)
  - Shell scripts will have descriptive functions and error messages
  - YAML will use consistent indentation (2 spaces) and structure
  - Comments will explain non-obvious Kubernetes configurations

### III. Test-First Development ⚠️ ADAPTED

- **Requirement**: TDD MUST be followed with Red-Green-Refactor
- **Status**: Infrastructure testing differs from application testing
- **Adaptation**:
  - Write verification scripts BEFORE creating Helm charts (test infrastructure)
  - Use `helm lint` and `helm template` for pre-deployment validation (red phase)
  - Deploy to Minikube and verify pods/services working (green phase)
  - Refactor Helm values for better configurability (refactor phase)
- **Justification**: Infrastructure-as-Code uses "deploy-verify" workflow rather than unit tests

### IV. Single Responsibility ✅ PASS

- **Requirement**: Each module, class, function has one clear purpose
- **Status**: Will structure Helm chart with clear separation
- **Compliance**:
  - Separate templates: frontend/deployment.yaml, backend/deployment.yaml, services, configmap, secret
  - Separate scripts: setup.sh (cluster), build-images.sh (images), deploy.sh (deployment)
  - Separate docs: DEPLOYMENT.md (how-to), TROUBLESHOOTING.md (issues), AI_DEVOPS.md (tools)

### V. Evolutionary Architecture ✅ PASS

- **Requirement**: Structure to support future phases while implementing only current requirements
- **Status**: Minikube deployment is stepping stone to cloud (Phase 5)
- **Compliance**:
  - Helm chart structure scales to production (just change values.yaml)
  - Use standard Kubernetes patterns (Deployments, Services, ConfigMaps)
  - Avoid Minikube-specific hacks that won't work in cloud
  - Document production readiness gaps (Ingress, HPA, monitoring)

### VI. User Experience First ✅ PASS

- **Requirement**: Interfaces MUST prioritize clarity and helpfulness
- **Status**: Deployment scripts and documentation are user-facing
- **Compliance**:
  - Scripts provide clear progress messages and error diagnostics
  - Documentation includes step-by-step guides with screenshots
  - Error messages suggest corrective actions (e.g., "Minikube not running. Run: minikube start")
  - Post-install NOTES.txt displays access URLs and next steps

**Overall Assessment**: ✅ PASS with adaptations
- TDD adapted for infrastructure testing (test scripts, then deploy, then verify)
- All other principles directly applicable and will be followed

## Project Structure

### Documentation (this feature)

```text
specs/004-kubernetes-deployment/
├── spec.md              # Feature specification (P1-P5 user stories)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Helm/Minikube/AI tools best practices
├── config-contracts.md  # Phase 1: ConfigMap/Secret/values.yaml schemas
├── quickstart.md        # Phase 1: Quick deployment guide
└── tasks.md             # Phase 2: Actionable implementation tasks (NOT created by /sp.plan)
```

### Source Code (repository root: phase-4-kubernetes-deployment/)

This feature adds Kubernetes deployment artifacts to the existing Phase 3 codebase.

**Existing Structure (Phase 3 - DO NOT MODIFY)**:
```text
backend/
├── src/
│   ├── main.py              # FastAPI app entry
│   ├── models/              # SQLModel database models
│   ├── services/            # Business logic (TodoManager, AuthService)
│   ├── agents/              # OpenAI Agents SDK agents
│   ├── tools/               # MCP tools for agents
│   └── api/                 # FastAPI routes
├── tests/                   # pytest test suite
├── Dockerfile               # Multi-stage Python build ✅ EXISTS
└── .dockerignore

frontend/
├── src/
│   ├── app/                 # Next.js 16 App Router pages
│   ├── components/          # React components
│   ├── lib/                 # Client libraries (ChatKit, auth)
│   └── auth.ts              # Better Auth configuration
├── public/                  # Static assets
├── tests/                   # Jest + RTL tests
├── Dockerfile               # Multi-stage Node.js build ✅ EXISTS
└── .dockerignore

docker-compose.yml           # Local dev setup ✅ EXISTS
.env.example                 # Environment template
```

**New Structure (Phase 4 - TO BE CREATED)**:
```text
k8s/                         # Kubernetes deployment resources
├── README.md                # Quick start guide
├── minikube/
│   ├── setup.sh             # Initialize Minikube cluster
│   ├── build-images.sh      # Build images in Minikube context
│   └── cleanup.sh           # Teardown script
├── kubectl-ai/
│   └── examples.md          # kubectl-ai usage examples
└── kagent/
    └── health-check.sh      # Automated cluster health check

helm/                        # Helm chart for deployment
└── todo-app/
    ├── Chart.yaml           # Chart metadata (v1.0.0, app v3.0.0)
    ├── values.yaml          # Default production values
    ├── values-dev.yaml      # Minikube-optimized overrides
    ├── .helmignore          # Exclude unnecessary files
    └── templates/
        ├── NOTES.txt        # Post-install instructions
        ├── _helpers.tpl     # Template helpers (labels, selectors)
        ├── frontend/
        │   ├── deployment.yaml   # Frontend Deployment
        │   └── service.yaml      # Frontend Service (NodePort 30300)
        ├── backend/
        │   ├── deployment.yaml   # Backend Deployment
        │   └── service.yaml      # Backend Service (ClusterIP 8000)
        └── shared/
            ├── configmap.yaml    # Non-sensitive config
            └── secret.yaml       # Sensitive credentials

scripts/
└── k8s/
    ├── deploy.sh            # One-command full deployment
    ├── verify.sh            # Post-deployment verification
    └── test.sh              # Automated acceptance tests

docs/
└── kubernetes/
    ├── DEPLOYMENT.md        # Step-by-step deployment guide
    ├── TROUBLESHOOTING.md   # Common issues and solutions
    └── AI_DEVOPS.md         # kubectl-ai, kagent, Docker AI usage
```

**Structure Decision**:
This is a **Web Application + Kubernetes Deployment** structure. The existing Phase 3 backend/frontend directories remain unchanged. All Kubernetes deployment artifacts are organized under new top-level directories (`k8s/`, `helm/`, `scripts/k8s/`, `docs/kubernetes/`) to maintain clean separation between application code and deployment infrastructure.

**Key Design Decisions**:
1. **Helm Chart Location**: `helm/todo-app/` at project root (standard Helm convention)
2. **Minikube Scripts**: `k8s/minikube/` for cluster management (setup, build, cleanup)
3. **Automation Scripts**: `scripts/k8s/` for deployment workflows (deploy, verify, test)
4. **Documentation**: `docs/kubernetes/` for comprehensive guides
5. **AI Tools Examples**: Under `k8s/kubectl-ai/` and `k8s/kagent/` for discoverability

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| TDD Adaptation | Infrastructure code requires "deploy-verify" workflow instead of unit testing | Pure TDD (write failing unit tests first) doesn't apply to Kubernetes manifests - we test by deploying and verifying, not mocking k8s API |

**Justification**: The adaptation maintains the *spirit* of TDD (test-first mindset, verification before proceeding) while acknowledging that infrastructure testing uses deployment verification rather than unit tests. We write verification scripts BEFORE creating Helm charts, deploy to verify, then refactor - this is the infrastructure equivalent of Red-Green-Refactor.

---

## Phase 0: Research & Technology Selection

**Goal**: Research Helm best practices, Minikube configuration, kubectl-ai/kagent capabilities, and resolve all "NEEDS CLARIFICATION" items.

### Research Tasks

#### 1. Helm Chart Best Practices for Microservices
**Question**: What is the recommended Helm chart structure for deploying multiple services (frontend + backend)?

**Research Areas**:
- Monolithic chart (single chart, multiple deployments) vs. umbrella chart (chart of charts)
- Template organization (_helpers.tpl patterns, subdirectories for services)
- values.yaml structure for multi-service configuration
- ConfigMap and Secret management patterns

**Expected Outcome**: Decision on chart structure + template organization pattern

---

#### 2. Minikube Docker Daemon Integration
**Question**: How to build and use Docker images in Minikube without external registry?

**Research Areas**:
- `eval $(minikube docker-env)` usage and persistence
- `imagePullPolicy: Never` vs. `imagePullPolicy: IfNotPresent`
- Image caching and rebuild workflows
- Troubleshooting image not found errors

**Expected Outcome**: Build script pattern + Deployment imagePullPolicy settings

---

#### 3. Kubernetes Health Probes Configuration
**Question**: What are the best practices for readinessProbe and livenessProbe configuration?

**Research Areas**:
- initialDelaySeconds for Node.js (Next.js) vs. Python (FastAPI) applications
- periodSeconds and failureThreshold for development vs. production
- httpGet vs. exec vs. tcpSocket probe types
- Impact of probe failures on pod lifecycle

**Expected Outcome**: Probe configuration template for both services

---

#### 4. Service-to-Service Communication in Kubernetes
**Question**: How do frontend and backend communicate when both are in the same Kubernetes cluster?

**Research Areas**:
- Kubernetes DNS resolution (`<service>.<namespace>.svc.cluster.local`)
- Environment variable injection for service discovery
- ClusterIP vs. NodePort for internal services
- CORS configuration for frontend-backend communication

**Expected Outcome**: Service configuration + environment variable mapping

---

#### 5. kubectl-ai Capabilities and Usage
**Question**: What operations can kubectl-ai assist with, and how do we integrate it?

**Research Areas**:
- Installation methods (pip, kubectl plugin)
- Common use cases (log analysis, troubleshooting, scaling)
- Prompt engineering for effective kubectl-ai queries
- Limitations and when to fall back to raw kubectl

**Expected Outcome**: Installation guide + 5+ practical examples

---

#### 6. kagent Features and Health Checks
**Question**: What cluster health checks can kagent automate?

**Research Areas**:
- Installation and configuration
- Built-in health check capabilities
- Custom check scripting
- Integration with monitoring tools (Prometheus, if applicable)

**Expected Outcome**: Health check script template

---

#### 7. Docker AI (Gordon) for Image Optimization
**Question**: How can Docker AI assist with image building and vulnerability scanning?

**Research Areas**:
- Docker Desktop AI features (version 4.53+ requirement)
- Dockerfile optimization suggestions
- Vulnerability scanning integration
- Build command enhancements

**Expected Outcome**: Documentation of Docker AI usage for this project

---

#### 8. Secrets Management in Helm
**Question**: How to securely pass secrets to Helm without committing them to git?

**Research Areas**:
- `helm install --set` for secrets at install time
- helm-secrets plugin for encrypted secrets in repo
- External secrets operators (for future Phase 5)
- `.helmignore` patterns to prevent secret leaks

**Expected Outcome**: Secret injection pattern for deployment scripts

---

**Deliverable**: `research.md` document with all decisions, rationales, and alternatives considered for each research task.

---

## Phase 1: Design & Configuration Contracts

**Prerequisites**: `research.md` complete with all technology decisions made

**Goal**: Design Helm chart structure, define configuration contracts (values schema, ConfigMap/Secret schemas), and create quick-start documentation.

### Design Artifacts

#### 1. Helm Values Schema (`config-contracts.md`)

Define the structure of `values.yaml` and `values-dev.yaml`:

**Schema Sections**:
```yaml
# Image Configuration
image:
  frontend:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never  # Minikube-specific
  backend:
    repository: todo-backend
    tag: latest
    pullPolicy: Never

# Service Configuration
service:
  frontend:
    type: NodePort
    port: 3000
    nodePort: 30300
  backend:
    type: ClusterIP
    port: 8000

# Resource Limits
resources:
  frontend:
    requests: {memory: "128Mi", cpu: "50m"}
    limits: {memory: "256Mi", cpu: "250m"}
  backend:
    requests: {memory: "128Mi", cpu: "50m"}
    limits: {memory: "256Mi", cpu: "250m"}

# Health Probes
healthProbe:
  frontend:
    readiness: {path: "/api/health", initialDelaySeconds: 10}
    liveness: {path: "/api/health", initialDelaySeconds: 30}
  backend:
    readiness: {path: "/api/health", initialDelaySeconds: 5}
    liveness: {path: "/api/health", initialDelaySeconds: 20}

# Configuration (non-sensitive)
config:
  BETTER_AUTH_URL: "http://frontend-service:3000"
  FRONTEND_URL: "http://frontend-service:3000"
  BACKEND_URL: "http://backend-service:8000"
  LLM_PROVIDER: "openai"
  OPENAI_DEFAULT_MODEL: "gpt-4o-mini"

# Secrets (sensitive - passed via --set)
secrets:
  DATABASE_URL: ""  # Required
  BETTER_AUTH_SECRET: ""  # Required (min 32 chars)
  OPENAI_API_KEY: ""  # Required
  CLOUDFLARE_R2_ACCOUNT_ID: ""
  CLOUDFLARE_R2_ACCESS_KEY_ID: ""
  CLOUDFLARE_R2_SECRET_ACCESS_KEY: ""
  CLOUDFLARE_R2_BUCKET_NAME: ""
```

**Validation Rules**:
- `secrets.DATABASE_URL` MUST be provided (fail if empty)
- `secrets.BETTER_AUTH_SECRET` MUST be ≥32 characters
- `secrets.OPENAI_API_KEY` MUST start with "sk-"
- Resource requests MUST be ≤ limits

---

#### 2. ConfigMap Contract

**File**: `helm/todo-app/templates/shared/configmap.yaml`

**Schema**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-app.fullname" . }}-config
data:
  BETTER_AUTH_URL: {{ .Values.config.BETTER_AUTH_URL | quote }}
  FRONTEND_URL: {{ .Values.config.FRONTEND_URL | quote }}
  BACKEND_URL: {{ .Values.config.BACKEND_URL | quote }}
  LLM_PROVIDER: {{ .Values.config.LLM_PROVIDER | quote }}
  OPENAI_DEFAULT_MODEL: {{ .Values.config.OPENAI_DEFAULT_MODEL | quote }}
  NEXT_PUBLIC_CHATKIT_API_URL: "/api/chat"
```

**Usage**: Mounted as environment variables in both frontend and backend Deployments

---

#### 3. Secret Contract

**File**: `helm/todo-app/templates/shared/secret.yaml`

**Schema**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-app.fullname" . }}-secrets
type: Opaque
stringData:
  DATABASE_URL: {{ required "secrets.DATABASE_URL is required" .Values.secrets.DATABASE_URL | quote }}
  BETTER_AUTH_SECRET: {{ required "secrets.BETTER_AUTH_SECRET is required" .Values.secrets.BETTER_AUTH_SECRET | quote }}
  OPENAI_API_KEY: {{ required "secrets.OPENAI_API_KEY is required" .Values.secrets.OPENAI_API_KEY | quote }}
  CLOUDFLARE_R2_ACCOUNT_ID: {{ .Values.secrets.CLOUDFLARE_R2_ACCOUNT_ID | quote }}
  CLOUDFLARE_R2_ACCESS_KEY_ID: {{ .Values.secrets.CLOUDFLARE_R2_ACCESS_KEY_ID | quote }}
  CLOUDFLARE_R2_SECRET_ACCESS_KEY: {{ .Values.secrets.CLOUDFLARE_R2_SECRET_ACCESS_KEY | quote }}
  CLOUDFLARE_R2_BUCKET_NAME: {{ .Values.secrets.CLOUDFLARE_R2_BUCKET_NAME | quote }}
```

**Validation**: Uses Helm's `required` function for mandatory secrets

---

#### 4. Deployment Contracts

**Frontend Deployment**:
- Replica count: 1 (dev), configurable via values
- Image: `todo-frontend:latest` with `imagePullPolicy: Never`
- Port: 3000
- Environment: ConfigMap + Secret refs
- Health probes: readiness + liveness on `/api/health`
- Resources: requests + limits from values

**Backend Deployment**:
- Replica count: 1 (dev), configurable via values
- Image: `todo-backend:latest` with `imagePullPolicy: Never`
- Port: 8000
- Environment: ConfigMap + Secret refs
- Health probes: readiness + liveness on `/api/health`
- Resources: requests + limits from values

---

#### 5. Service Contracts

**Frontend Service**:
```yaml
type: NodePort
port: 3000
targetPort: 3000
nodePort: 30300
```
- External access via `http://$(minikube ip):30300`

**Backend Service**:
```yaml
type: ClusterIP
port: 8000
targetPort: 8000
```
- Internal access via `http://backend-service:8000`

---

#### 6. Quick Start Guide (`quickstart.md`)

**Sections**:
1. Prerequisites Check (Docker, Minikube, Helm, kubectl)
2. One-Command Deployment
   ```bash
   ./scripts/k8s/deploy.sh
   ```
3. Manual Step-by-Step (for learning)
   - Start Minikube
   - Build images
   - Install Helm chart
   - Verify deployment
4. Access the Application
5. Common Issues (with solutions)
6. Teardown

---

#### 7. Agent Context Update

Run the agent context update script:
```bash
../.specify/scripts/bash/update-agent-context.sh claude
```

This will:
- Detect we're using Claude Code
- Update `.specify/memory/agent-specific/claude.md` or similar
- Add Phase 4 technologies to the stack:
  - Kubernetes 1.28+
  - Minikube 1.32+
  - Helm 3.x
  - kubectl-ai, kagent, Docker AI
- Preserve any manual additions between markers

---

**Deliverables**:
- `config-contracts.md` - Complete values.yaml schema with validation rules
- `quickstart.md` - Quick deployment guide
- Updated agent context file with Phase 4 technologies

---

## Phase 2: Task Breakdown (Separate Command)

**Note**: Phase 2 (task breakdown) is handled by the `/sp.tasks` command, which is run AFTER this `/sp.plan` command completes.

The `/sp.tasks` command will read this plan and generate `tasks.md` with:
- Granular implementation tasks (1-4 hours each)
- Test-first workflow for each task
- Dependency ordering
- Acceptance criteria

**Not included in `/sp.plan` output.**

---

## Architecture Decision Records (ADRs)

After completing Phase 0 research and Phase 1 design, evaluate whether any decisions meet the ADR significance criteria:

**ADR Test (all must be TRUE)**:
1. **Impact**: Does it have long-term consequences? (framework, data model, API, security, platform)
2. **Alternatives**: Were multiple viable options considered with tradeoffs?
3. **Scope**: Is it cross-cutting and influences system design?

**Likely ADR Candidates from This Plan**:

### ADR-001: Monolithic Helm Chart vs. Umbrella Chart
- **Decision**: Use monolithic chart with modular templates
- **Rationale**: Simpler deployment, shared configuration, easier service discovery
- **Alternatives**: Umbrella chart (separate charts for frontend/backend), raw manifests
- **Significance**: ✅ Affects deployment architecture, Helm chart maintainability, and scalability to Phase 5

### ADR-002: Minikube Docker Daemon vs. External Registry
- **Decision**: Build images in Minikube's Docker daemon
- **Rationale**: Zero setup, fast iteration, no registry overhead, development-optimized
- **Alternatives**: Docker Hub, GitHub Container Registry, local registry in Minikube
- **Significance**: ✅ Affects build workflow, image availability, and transition to production

### ADR-003: NodePort vs. Ingress for Frontend Exposure
- **Decision**: Use NodePort for development, document Ingress for production
- **Rationale**: NodePort simpler for Minikube, Ingress requires additional setup (minikube tunnel)
- **Alternatives**: LoadBalancer (requires MetalLB), Ingress (requires ingress controller)
- **Significance**: ✅ Affects access patterns, production readiness, and external integration

**Suggested Action**: After plan approval, run `/sp.adr` for each candidate:
```bash
/sp.adr "Monolithic Helm Chart for Multi-Service Deployment"
/sp.adr "Minikube Docker Daemon for Local Development"
/sp.adr "NodePort Service Exposure for Development Environment"
```

---

## Summary

This plan establishes the architecture for Phase 4: Local Kubernetes Deployment. The approach prioritizes:

1. **Simplicity**: Monolithic Helm chart, Minikube Docker daemon, NodePort exposure
2. **Production Readiness**: Standard Kubernetes patterns that scale to cloud (Phase 5)
3. **Developer Experience**: One-command deployment, AI-assisted operations, comprehensive docs
4. **Security**: Proper secret management, no credentials in git
5. **Evolutionary Architecture**: Deployment infrastructure that supports future cloud migration

**Next Steps**:
1. Execute Phase 0 research to resolve all technology questions
2. Complete Phase 1 design to create configuration contracts and quick-start guide
3. Run `/sp.tasks` to generate granular implementation tasks
4. Consider documenting ADRs for significant architectural decisions
5. Begin implementation using `/sp.implement` with Red-Green-Refactor workflow

**Success Metrics** (from spec.md):
- Pods ready in <2 minutes
- Frontend accessible and loads in <5 seconds
- End-to-end user flows working (login, chat, todos)
- Health probes detect failures and auto-restart in <30 seconds
- One-command deployment completes in <10 minutes
- AI DevOps tools documented with 5+ verified examples
