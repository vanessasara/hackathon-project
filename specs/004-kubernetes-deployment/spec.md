# Feature Specification: Local Kubernetes Deployment

**Feature Branch**: `004-kubernetes-deployment`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Local Kubernetes Deployment with Helm and AI DevOps Tools"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Deploy Application on Minikube (Priority: P1)

As a DevOps engineer, I want to deploy the Phase 3 Todo Chatbot application (Next.js frontend + FastAPI backend) on a local Minikube cluster using Helm charts, so that I can test and validate Kubernetes deployment configurations before production.

**Why this priority**: This is the foundational capability. Without basic deployment working, no other stories can be completed. It represents the core MVP - getting the application running in Kubernetes locally.

**Independent Test**: Can be fully tested by running `helm install todo-app ./helm/todo-app` and verifying both pods are running and the frontend is accessible via browser at `http://$(minikube ip):30300`. Delivers immediate value by proving Kubernetes deployment viability.

**Acceptance Scenarios**:

1. **Given** I have a working Minikube cluster and the Phase 3 application source code, **When** I run the Helm install command with required secrets, **Then** both frontend and backend pods should reach Ready state (2/2 containers running)
2. **Given** both pods are running, **When** I access the frontend via NodePort on port 30300, **Then** I should see the Todo Chatbot UI and be able to interact with it
3. **Given** the application is deployed, **When** I check the backend logs, **Then** I should see successful database connections to Neon PostgreSQL and no authentication errors
4. **Given** the services are configured, **When** the frontend makes API calls to the backend, **Then** the backend should respond successfully (verified in browser network tab)
5. **Given** I update the application code, **When** I rebuild the Docker images and perform a rolling update, **Then** the new version should deploy without downtime

---

### User Story 2 - Reliable Health Checks (Priority: P2)

As a platform engineer, I want both frontend and backend pods to have properly configured readiness and liveness probes, so that Kubernetes can automatically detect and restart unhealthy containers, ensuring high availability.

**Why this priority**: Once deployment works (P1), reliability is the next critical concern. Health checks enable automatic recovery and prevent broken pods from serving traffic, which is essential for production readiness.

**Independent Test**: Can be tested by deploying the application, then simulating failures (e.g., killing processes inside containers, breaking database connections) and observing that Kubernetes automatically restarts unhealthy pods. Delivers value by proving resilience.

**Acceptance Scenarios**:

1. **Given** the backend pod is starting, **When** Kubernetes checks the readiness probe at `/api/health`, **Then** the pod should not receive traffic until the probe returns 200 OK
2. **Given** the frontend pod is running, **When** I manually kill the Next.js process inside the container, **Then** the liveness probe should fail and Kubernetes should automatically restart the pod within 30 seconds
3. **Given** the backend loses database connectivity, **When** the health endpoint is called, **Then** it should return a failure status and the pod should be marked as not ready
4. **Given** both pods are healthy, **When** I check `kubectl get pods`, **Then** both should show READY status as "1/1" or "2/2"

---

### User Story 3 - Secure Configuration Management (Priority: P3)

As a security-conscious developer, I want sensitive configuration (API keys, database passwords) stored in Kubernetes Secrets and non-sensitive configuration in ConfigMaps, so that credentials are never exposed in version control or logs.

**Why this priority**: While important for security best practices, the application can technically run with environment variables passed directly. This is elevated to P3 because proper secrets management is critical before any production deployment.

**Independent Test**: Can be tested by creating ConfigMaps and Secrets, verifying environment variables are properly injected into pods, and confirming secrets are base64 encoded in etcd. Delivers value by establishing security baseline.

**Acceptance Scenarios**:

1. **Given** I have a `.env` file with all required secrets, **When** I install the Helm chart with `--set secrets.*` flags, **Then** a Kubernetes Secret should be created with all sensitive values base64 encoded
2. **Given** the ConfigMap contains `BETTER_AUTH_URL` and `BACKEND_URL`, **When** pods start, **Then** these environment variables should be available inside the containers (verified with `kubectl exec`)
3. **Given** the Secret contains `DATABASE_URL` and `OPENAI_API_KEY`, **When** I view the Secret with `kubectl get secret todo-secrets -o yaml`, **Then** the values should be base64 encoded and not plaintext
4. **Given** I need to update a configuration value, **When** I modify the ConfigMap and restart the pods, **Then** the new value should be picked up without requiring Helm chart changes
5. **Given** the application is running, **When** I check pod logs, **Then** no secrets or API keys should be visible in plaintext

---

### User Story 4 - AI-Assisted Operations (Priority: P4)

As a DevOps engineer learning Kubernetes, I want documented examples of using kubectl-ai and kagent for cluster operations, so that I can leverage AI assistance for troubleshooting and operations tasks instead of memorizing complex kubectl commands.

**Why this priority**: This is a nice-to-have enhancement that improves developer experience but isn't required for the application to function. It represents tooling optimization rather than core functionality.

**Independent Test**: Can be tested by running the documented kubectl-ai and kagent commands and verifying they produce useful outputs (e.g., kubectl-ai can scale deployments, kagent can analyze cluster health). Delivers value by reducing operational complexity.

**Acceptance Scenarios**:

1. **Given** kubectl-ai is installed, **When** I run `kubectl-ai "show me logs from pods with errors"`, **Then** it should automatically execute the appropriate kubectl command and display error logs
2. **Given** kagent is installed, **When** I run `kagent "analyze cluster health for todo-app namespace"`, **Then** it should provide a summary of resource usage, pod status, and any detected issues
3. **Given** I have Docker Desktop 4.53+ with AI features, **When** I run `docker ai "scan todo-frontend:latest for vulnerabilities"`, **Then** it should perform a security scan and report findings
4. **Given** the application has a configuration issue, **When** I use kubectl-ai to diagnose, **Then** it should suggest the root cause and remediation steps

---

### User Story 5 - One-Command Deployment Experience (Priority: P5)

As a developer who wants to iterate quickly, I want a single script (`./scripts/k8s/deploy.sh`) that sets up Minikube, builds images, and deploys the application, so that I can go from source code to running application in one command.

**Why this priority**: This is a convenience feature that improves developer productivity but isn't essential for the deployment itself to work. It's automation of steps that can be performed manually.

**Independent Test**: Can be tested by running `./scripts/k8s/deploy.sh` on a clean machine with only Docker installed, and verifying the entire stack comes up successfully. Delivers value by reducing setup friction.

**Acceptance Scenarios**:

1. **Given** I have Docker installed but no Minikube, **When** I run `./scripts/k8s/deploy.sh`, **Then** the script should start Minikube, build images, create namespaces, and deploy the application
2. **Given** the script encounters missing prerequisites (e.g., helm not installed), **When** it runs the prerequisite check, **Then** it should display clear error messages with installation instructions
3. **Given** the script completes successfully, **When** it finishes, **Then** it should display the frontend URL and instructions for accessing the application
4. **Given** I need to tear down the environment, **When** I run `./scripts/k8s/cleanup.sh`, **Then** it should cleanly remove all resources and stop Minikube

---

### Edge Cases

- What happens when Minikube runs out of memory or disk space? (Should fail gracefully with clear error messages)
- How does the system handle connection failures to external services (Neon DB, Cloudflare R2)? (Pods should remain in NotReady state until connectivity is restored)
- What if the Docker daemon inside Minikube is not accessible? (Build script should detect this and instruct user to run `eval $(minikube docker-env)`)
- What if required secrets are not provided during Helm installation? (Helm should fail with validation errors before creating resources)
- How are pod restarts handled during database migrations? (Should use initContainers for migrations to ensure they complete before app starts)
- What if the NodePort is already in use by another service? (Kubernetes should fail to create the service with a clear error message)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST deploy the Phase 3 Todo Chatbot (Next.js 16 frontend + FastAPI backend) on a local Minikube Kubernetes cluster
- **FR-002**: System MUST use Helm charts for declarative deployment configuration with separate `values.yaml` and `values-dev.yaml` files
- **FR-003**: System MUST build Docker images directly in Minikube's Docker daemon using `eval $(minikube docker-env)` and set `imagePullPolicy: Never`
- **FR-004**: System MUST expose the frontend service via NodePort on port 30300 for external browser access
- **FR-005**: System MUST keep the backend service as ClusterIP (internal only) and proxy API calls through the frontend
- **FR-006**: System MUST implement readiness probes at `/api/health` for both frontend and backend with appropriate initial delays
- **FR-007**: System MUST implement liveness probes at `/api/health` for both frontend and backend to enable automatic restart on failures
- **FR-008**: System MUST separate configuration into ConfigMaps (non-sensitive: BETTER_AUTH_URL, FRONTEND_URL, BACKEND_URL, LLM_PROVIDER, OPENAI_DEFAULT_MODEL) and Secrets (sensitive: DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, CLOUDFLARE_R2_*)
- **FR-009**: System MUST create a health endpoint at `/api/health` in the Next.js frontend (currently missing, exists in backend)
- **FR-010**: System MUST enable frontend-to-backend communication using Kubernetes DNS: `http://backend-service:8000`
- **FR-011**: System MUST enable backend-to-frontend communication for JWKS fetching using Kubernetes DNS: `http://frontend-service:3000`
- **FR-012**: System MUST set resource limits (requests: 128Mi/50m, limits: 256Mi/250m) to prevent resource exhaustion
- **FR-013**: System MUST provide automation scripts for setup (`k8s/minikube/setup.sh`), image building (`k8s/minikube/build-images.sh`), and cleanup (`k8s/minikube/cleanup.sh`)
- **FR-014**: System MUST provide a one-command deployment script at `scripts/k8s/deploy.sh` that handles the full setup workflow
- **FR-015**: System MUST document kubectl-ai usage examples in `k8s/kubectl-ai/examples.md` for common operations (scaling, troubleshooting, log viewing)
- **FR-016**: System MUST document kagent usage in `k8s/kagent/health-check.sh` for automated cluster health checks
- **FR-017**: System MUST document Docker AI (Gordon) usage in `docs/kubernetes/AI_DEVOPS.md` for vulnerability scanning and optimization suggestions
- **FR-018**: System MUST provide comprehensive documentation including deployment guide, troubleshooting, and AI DevOps tools usage

### Key Entities *(include if feature involves data)*

- **Kubernetes Pod**: Represents a running instance of the frontend or backend application container with health probes and resource limits
- **Kubernetes Service**: Represents network access configuration (NodePort for frontend at 30300, ClusterIP for backend at 8000)
- **Kubernetes ConfigMap**: Stores non-sensitive configuration key-value pairs (URLs, provider names, model names) mounted as environment variables
- **Kubernetes Secret**: Stores sensitive credentials (database URLs, API keys, auth secrets) mounted as environment variables with base64 encoding
- **Helm Chart**: Package containing all Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets) with templating for reusable configurations
- **Minikube Cluster**: Local single-node Kubernetes cluster for development and testing with 4 CPUs, 8GB RAM, 20GB disk
- **Docker Image**: Container image for frontend (todo-frontend:latest) and backend (todo-backend:latest) built from existing Dockerfiles

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Both frontend and backend pods reach Ready state (1/1 or 2/2) within 2 minutes of Helm installation on a fresh Minikube cluster
- **SC-002**: Frontend is accessible via browser at `http://$(minikube ip):30300` and loads the chat interface within 5 seconds
- **SC-003**: User can successfully login, chat with AI agent, and create/view todos without errors (end-to-end flow works)
- **SC-004**: Health probes successfully detect failures - when a process is killed, the pod restarts automatically within 30 seconds
- **SC-005**: No secrets or API keys are visible in plaintext when inspecting pods, ConfigMaps, or logs
- **SC-006**: The one-command deployment script (`./scripts/k8s/deploy.sh`) completes successfully from a clean state in under 10 minutes
- **SC-007**: Documentation is complete with step-by-step guides for deployment, verification, troubleshooting, and AI tools usage
- **SC-008**: At least 5 kubectl-ai command examples are documented and verified to work correctly
- **SC-009**: kagent health check script successfully analyzes the cluster and reports status without errors
- **SC-010**: All Phase 4 hackathon requirements are met: Minikube deployment, Helm charts, health checks, configuration management, AI DevOps tools integration

### Technical Constraints

- Must use Minikube (not other Kubernetes distributions like k3s, kind, or cloud providers)
- Must build images in Minikube's Docker daemon (not use external registries like Docker Hub or ECR)
- Must use Helm 3.x for chart management (not Helm 2 or raw Kubernetes manifests)
- Must maintain compatibility with existing Phase 3 application code (no breaking changes to frontend/backend)
- Must connect to external Neon PostgreSQL database (not deploy database in Kubernetes)
- Must connect to external Cloudflare R2 storage (not deploy object storage in Kubernetes)
- Must support Linux/WSL2 environment (user's current setup)
- Must document AI DevOps tools: kubectl-ai, kagent, Docker AI (Gordon)

### Out of Scope

- Production Kubernetes deployment (EKS, GKE, AKS)
- Ingress controller configuration (use NodePort for simplicity)
- Horizontal Pod Autoscaler (HPA) - optional nice-to-have
- Persistent volumes for application data (using external database)
- Service mesh (Istio, Linkerd)
- CI/CD pipeline integration (GitHub Actions, GitLab CI)
- Monitoring stack (Prometheus, Grafana)
- Log aggregation (ELK, Loki)
- Multi-region or multi-cluster deployment
- Automated database migrations in Kubernetes (run manually if needed)

### Assumptions

- User has Docker installed and working on Linux/WSL2
- User has at least 8GB RAM available for Minikube
- User has Phase 3 application working locally with docker-compose
- User has `.env` file with all required secrets (DATABASE_URL, OPENAI_API_KEY, etc.)
- External services (Neon DB, Cloudflare R2) are accessible from Minikube pods
- User has basic familiarity with Kubernetes concepts (pods, services, deployments)
- User can install additional tools (kubectl, helm, minikube) if not already present
