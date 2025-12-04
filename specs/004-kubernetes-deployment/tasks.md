---
description: "Task list for Phase 4: Local Kubernetes Deployment"
---

# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/004-kubernetes-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No test tasks included - infrastructure validation done via deployment verification scripts

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

This is a **Web Application + Kubernetes Deployment** project:
- **Existing** (Phase 3 - do not modify): `backend/`, `frontend/`, `docker-compose.yml`
- **New** (Phase 4): `k8s/`, `helm/`, `scripts/k8s/`, `docs/kubernetes/`

---

## Phase 1: Setup (Project Structure)

**Purpose**: Create directory structure and verify prerequisites

- [X] T001 Verify Minikube, Helm, kubectl, Docker prerequisites are installed
- [X] T002 [P] Create k8s/ directory structure (k8s/minikube/, k8s/kubectl-ai/, k8s/kagent/)
- [X] T003 [P] Create helm/todo-app/ directory structure (templates/frontend/, templates/backend/, templates/shared/)
- [X] T004 [P] Create scripts/k8s/ directory for automation scripts
- [X] T005 [P] Create docs/kubernetes/ directory for documentation
- [X] T006 [P] Create Helm Chart.yaml metadata file at helm/todo-app/Chart.yaml
- [X] T007 [P] Create .helmignore file at helm/todo-app/.helmignore
- [X] T008 [P] Create Helm _helpers.tpl template at helm/todo-app/templates/_helpers.tpl

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 Create Minikube cluster setup script at k8s/minikube/setup.sh
- [X] T010 Create Minikube image build script at k8s/minikube/build-images.sh
- [X] T011 [P] Create Minikube cleanup script at k8s/minikube/cleanup.sh
- [X] T012 [P] Create base Helm values.yaml at helm/todo-app/values.yaml
- [X] T013 [P] Create Minikube-optimized values-dev.yaml at helm/todo-app/values-dev.yaml
- [ ] T014 Execute setup.sh to initialize Minikube cluster (4 CPUs, 8GB RAM, 20GB disk)
- [ ] T015 Execute build-images.sh to build frontend and backend Docker images in Minikube context

**Checkpoint**: Foundation ready - Minikube running, images built, Helm chart scaffolded

---

## Phase 3: User Story 1 - Deploy Application on Minikube (Priority: P1) 🎯 MVP

**Goal**: Basic deployment of frontend and backend to Minikube with services accessible

**Independent Test**: Run `helm install todo-app ./helm/todo-app -f helm/todo-app/values-dev.yaml --set secrets.*` and verify both pods reach Ready state, frontend accessible at `http://$(minikube ip):30300`

### Implementation for User Story 1

- [X] T016 [P] [US1] Create frontend Deployment template at helm/todo-app/templates/frontend/deployment.yaml
- [X] T017 [P] [US1] Create backend Deployment template at helm/todo-app/templates/backend/deployment.yaml
- [X] T018 [P] [US1] Create frontend NodePort Service template at helm/todo-app/templates/frontend/service.yaml
- [X] T019 [P] [US1] Create backend ClusterIP Service template at helm/todo-app/templates/backend/service.yaml
- [X] T020 [P] [US1] Create ConfigMap template at helm/todo-app/templates/shared/configmap.yaml
- [X] T021 [P] [US1] Create Secret template with validation at helm/todo-app/templates/shared/secret.yaml
- [ ] T022 [US1] Deploy Helm chart with secrets from .env file (helm install todo-app ...)
- [ ] T023 [US1] Verify both pods reach Ready state within 2 minutes (kubectl get pods -n todo-app)
- [ ] T024 [US1] Verify frontend accessible via NodePort 30300 in browser
- [ ] T025 [US1] Verify backend accessible internally (kubectl exec ... curl backend-service:8000)
- [ ] T026 [US1] Test end-to-end user flow (login, chat, create todo)

**Checkpoint**: At this point, the application should be fully deployed and functional on Minikube

---

## Phase 4: User Story 2 - Reliable Health Checks (Priority: P2)

**Goal**: Implement readiness and liveness probes for automatic failure detection and recovery

**Independent Test**: Kill a pod process and verify Kubernetes automatically restarts it within 30 seconds, verify pods don't receive traffic until health checks pass

### Implementation for User Story 2

- [X] T027 [US2] Create frontend health endpoint at frontend/src/app/api/health/route.ts
- [X] T028 [US2] Add readiness probe configuration to frontend Deployment (helm/todo-app/templates/frontend/deployment.yaml)
- [X] T029 [US2] Add liveness probe configuration to frontend Deployment (helm/todo-app/templates/frontend/deployment.yaml)
- [X] T030 [US2] Add readiness probe configuration to backend Deployment (helm/todo-app/templates/backend/deployment.yaml)
- [X] T031 [US2] Add liveness probe configuration to backend Deployment (helm/todo-app/templates/backend/deployment.yaml)
- [X] T032 [US2] Update values.yaml with health probe settings (initialDelaySeconds, periodSeconds)
- [ ] T033 [US2] Rebuild frontend image with health endpoint (k8s/minikube/build-images.sh)
- [ ] T034 [US2] Upgrade Helm release with health probes (helm upgrade todo-app ...)
- [ ] T035 [US2] Test readiness probe (verify pod not ready until health check passes)
- [ ] T036 [US2] Test liveness probe (kill process, verify auto-restart within 30 seconds)

**Checkpoint**: Health probes working - automatic failure detection and recovery functional

---

## Phase 5: User Story 3 - Secure Configuration Management (Priority: P3)

**Goal**: Separate sensitive configuration (Secrets) from non-sensitive (ConfigMap) with proper base64 encoding

**Independent Test**: Verify environment variables properly injected into pods, secrets base64 encoded in etcd, no plaintext secrets in logs

### Implementation for User Story 3

- [ ] T037 [US3] Review and validate ConfigMap data section (non-sensitive: BETTER_AUTH_URL, FRONTEND_URL, BACKEND_URL, LLM_PROVIDER, OPENAI_DEFAULT_MODEL)
- [ ] T038 [US3] Review and validate Secret stringData section (sensitive: DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, R2 credentials)
- [ ] T039 [US3] Add required validation for mandatory secrets (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY)
- [ ] T040 [US3] Configure environment variable injection from ConfigMap in frontend Deployment
- [ ] T041 [US3] Configure environment variable injection from ConfigMap in backend Deployment
- [ ] T042 [US3] Configure environment variable injection from Secret in frontend Deployment
- [ ] T043 [US3] Configure environment variable injection from Secret in backend Deployment
- [ ] T044 [US3] Upgrade Helm release with proper ConfigMap/Secret mounting
- [ ] T045 [US3] Verify ConfigMap values visible in pod (kubectl exec ... env | grep BETTER_AUTH_URL)
- [ ] T046 [US3] Verify Secret values base64 encoded (kubectl get secret todo-secrets -o yaml)
- [ ] T047 [US3] Verify no secrets in pod logs (kubectl logs deployment/todo-app-frontend | grep -v "sk-")

**Checkpoint**: Configuration management secure - secrets properly separated and encoded

---

## Phase 6: User Story 4 - AI-Assisted Operations (Priority: P4)

**Goal**: Document kubectl-ai, kagent, and Docker AI usage with practical examples

**Independent Test**: Run documented kubectl-ai and kagent commands and verify they produce useful outputs

### Implementation for User Story 4

- [ ] T048 [P] [US4] Document kubectl-ai installation in docs/kubernetes/AI_DEVOPS.md
- [ ] T049 [P] [US4] Document kagent installation in docs/kubernetes/AI_DEVOPS.md
- [ ] T050 [P] [US4] Document Docker AI features in docs/kubernetes/AI_DEVOPS.md
- [ ] T051 [P] [US4] Create kubectl-ai examples for log analysis in k8s/kubectl-ai/examples.md
- [ ] T052 [P] [US4] Create kubectl-ai examples for troubleshooting in k8s/kubectl-ai/examples.md
- [ ] T053 [P] [US4] Create kubectl-ai examples for scaling operations in k8s/kubectl-ai/examples.md
- [ ] T054 [P] [US4] Create kubectl-ai examples for resource inspection in k8s/kubectl-ai/examples.md
- [ ] T055 [P] [US4] Create kubectl-ai examples for debugging failures in k8s/kubectl-ai/examples.md
- [ ] T056 [US4] Create kagent health check script at k8s/kagent/health-check.sh
- [ ] T057 [US4] Install kubectl-ai (pip install kubectl-ai or kubectl plugin)
- [ ] T058 [US4] Install kagent (pip install kagent)
- [ ] T059 [US4] Verify kubectl-ai command examples work (test 5+ examples)
- [ ] T060 [US4] Verify kagent health check script works (k8s/kagent/health-check.sh)
- [ ] T061 [US4] Document Docker AI vulnerability scanning usage

**Checkpoint**: AI DevOps tools documented with verified examples

---

## Phase 7: User Story 5 - One-Command Deployment Experience (Priority: P5)

**Goal**: Create automation scripts for complete deployment workflow from source to running application

**Independent Test**: Run `./scripts/k8s/deploy.sh` on clean machine and verify entire stack comes up successfully in under 10 minutes

### Implementation for User Story 5

- [X] T062 [US5] Create deploy.sh script at scripts/k8s/deploy.sh (setup, build, deploy workflow)
- [X] T063 [US5] Add prerequisites check to deploy.sh (Docker, Minikube, Helm, kubectl)
- [X] T064 [US5] Add Minikube status check and auto-start to deploy.sh
- [X] T065 [US5] Add image building step to deploy.sh (calls k8s/minikube/build-images.sh)
- [X] T066 [US5] Add namespace creation to deploy.sh (kubectl create namespace todo-app)
- [X] T067 [US5] Add secret loading from .env to deploy.sh (source .env and helm --set)
- [X] T068 [US5] Add Helm install/upgrade logic to deploy.sh
- [X] T069 [US5] Add deployment verification to deploy.sh (poll pod status)
- [X] T070 [US5] Add access URL display to deploy.sh (show http://$(minikube ip):30300)
- [ ] T071 [P] [US5] Create verify.sh script at scripts/k8s/verify.sh (post-deployment checks)
- [ ] T072 [P] [US5] Create test.sh script at scripts/k8s/test.sh (automated acceptance tests)
- [ ] T073 [US5] Test deploy.sh from clean state (minikube delete first)
- [ ] T074 [US5] Verify deployment completes in under 10 minutes
- [ ] T075 [US5] Test verify.sh script (pod status, health endpoints, connectivity)
- [ ] T076 [US5] Test test.sh script (automated end-to-end validation)

**Checkpoint**: One-command deployment working - complete automation functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and production readiness notes

- [X] T077 [P] Create Helm NOTES.txt at helm/todo-app/templates/NOTES.txt (post-install instructions)
- [X] T078 [P] Create step-by-step deployment guide at docs/kubernetes/DEPLOYMENT.md
- [ ] T079 [P] Create troubleshooting guide at docs/kubernetes/TROUBLESHOOTING.md
- [X] T080 [P] Create quick start README at k8s/README.md
- [ ] T081 [P] Update Phase 4 .env.example with all required Kubernetes environment variables
- [X] T082 [P] Add resource limits to frontend Deployment (requests: 128Mi/50m, limits: 256Mi/250m)
- [X] T083 [P] Add resource limits to backend Deployment (requests: 128Mi/50m, limits: 256Mi/250m)
- [X] T084 [P] Document production readiness gaps (Ingress, HPA, monitoring) in docs/kubernetes/DEPLOYMENT.md
- [X] T085 [P] Document Phase 5 migration path (cloud Kubernetes) in docs/kubernetes/DEPLOYMENT.md
- [ ] T086 Create quickstart.md at specs/004-kubernetes-deployment/quickstart.md
- [ ] T087 Validate entire deployment workflow end-to-end (clean slate to working app)
- [ ] T088 Run final verification: all 5 user stories independently testable
- [ ] T089 Document known issues and limitations in docs/kubernetes/TROUBLESHOOTING.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Deploy) → BLOCKS US2, US3 (need deployment first)
  - US2 (Health Checks) → Can proceed after US1
  - US3 (Config Management) → Can proceed after US1
  - US4 (AI DevOps) → Can proceed after US1 (independent)
  - US5 (Automation) → Should be last (wraps all previous stories)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Deploy - P1)**: Must complete first - provides base deployment for all others
- **US2 (Health Checks - P2)**: Depends on US1 (modifies existing deployment)
- **US3 (Config Management - P3)**: Depends on US1 (modifies existing deployment)
- **US4 (AI DevOps - P4)**: Depends on US1 (needs working cluster), independent otherwise
- **US5 (Automation - P5)**: Depends on US1-4 (automates all previous stories)

### Within Each User Story

- Setup/Foundational: Complete before user stories
- Helm templates before deployment
- Deployment before verification
- Manual steps before automation
- Core implementation before documentation

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks marked [P] can run in parallel (T002-T008)

**Phase 2 (Foundational)**: T010, T011, T012, T013 can run in parallel after T009

**Phase 3 (US1)**: T016-T021 (all Helm templates) can be created in parallel

**Phase 4 (US2)**: T028-T031 (probe configurations) can be done in parallel after T027

**Phase 5 (US3)**: T040-T043 (environment variable configurations) can be done in parallel

**Phase 6 (US4)**: T048-T055 (all documentation tasks) can be done in parallel

**Phase 7 (US5)**: T071-T072 (verify.sh and test.sh) can be created in parallel with deploy.sh work

**Phase 8 (Polish)**: T077-T085 (all documentation) can be done in parallel

---

## Parallel Example: User Story 1 (Deploy Application)

```bash
# Launch all Helm template creation tasks together:
Task: "Create frontend Deployment template at helm/todo-app/templates/frontend/deployment.yaml"
Task: "Create backend Deployment template at helm/todo-app/templates/backend/deployment.yaml"
Task: "Create frontend NodePort Service template at helm/todo-app/templates/frontend/service.yaml"
Task: "Create backend ClusterIP Service template at helm/todo-app/templates/backend/service.yaml"
Task: "Create ConfigMap template at helm/todo-app/templates/shared/configmap.yaml"
Task: "Create Secret template at helm/todo-app/templates/shared/secret.yaml"
```

## Parallel Example: User Story 4 (AI DevOps)

```bash
# Launch all kubectl-ai example documentation tasks together:
Task: "Create kubectl-ai examples for log analysis in k8s/kubectl-ai/examples.md"
Task: "Create kubectl-ai examples for troubleshooting in k8s/kubectl-ai/examples.md"
Task: "Create kubectl-ai examples for scaling operations in k8s/kubectl-ai/examples.md"
Task: "Create kubectl-ai examples for resource inspection in k8s/kubectl-ai/examples.md"
Task: "Create kubectl-ai examples for debugging failures in k8s/kubectl-ai/examples.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T015) - CRITICAL
3. Complete Phase 3: User Story 1 (T016-T026)
4. **STOP and VALIDATE**: Test deployment independently
   - Verify pods running
   - Verify frontend accessible
   - Test login and chat functionality
5. Deploy/demo MVP if ready

**Result**: Working Kubernetes deployment on Minikube with basic functionality

### Incremental Delivery

1. Complete Setup + Foundational → Infrastructure ready
2. Add US1 (Deploy) → Test independently → **MVP delivered!**
3. Add US2 (Health Checks) → Test auto-restart → Deploy/Demo
4. Add US3 (Config Management) → Verify secrets secure → Deploy/Demo
5. Add US4 (AI DevOps) → Document tools → Deploy/Demo
6. Add US5 (Automation) → One-command deployment → Deploy/Demo
7. Polish → Complete documentation → **Production-ready!**

**Each story adds value incrementally**

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T015)
2. Once Foundational is done:
   - **Developer A**: US1 (Deploy) - T016-T026
   - Wait for US1 completion (blocks others)
3. After US1 complete:
   - **Developer A**: US2 (Health Checks) - T027-T036
   - **Developer B**: US4 (AI DevOps) - T048-T061 (independent)
4. After US2 complete:
   - **Developer A**: US3 (Config Management) - T037-T047
   - **Developer B**: Continue US4
5. After US3 and US4 complete:
   - **Developer A**: US5 (Automation) - T062-T076
   - **Developer B**: Polish - T077-T089
6. Final validation together

**Result**: Parallelized where possible, respecting dependencies

---

## Acceptance Criteria

### User Story 1 - Deploy Application on Minikube ✅

- [ ] Both frontend and backend pods reach Ready state (1/1 or 2/2) within 2 minutes
- [ ] Frontend accessible via `http://$(minikube ip):30300`
- [ ] Backend accessible internally at `http://backend-service:8000`
- [ ] User can login, chat with AI, and create todos
- [ ] Rolling update works when rebuilding images

### User Story 2 - Reliable Health Checks ✅

- [ ] Readiness probes configured for both services at `/api/health`
- [ ] Liveness probes configured for both services at `/api/health`
- [ ] Pods don't receive traffic until health checks pass
- [ ] Killing a pod process triggers auto-restart within 30 seconds
- [ ] Frontend health endpoint created and functional

### User Story 3 - Secure Configuration Management ✅

- [ ] ConfigMap contains non-sensitive config (BETTER_AUTH_URL, FRONTEND_URL, BACKEND_URL, LLM_PROVIDER, OPENAI_DEFAULT_MODEL)
- [ ] Secret contains sensitive config (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, R2 credentials)
- [ ] Secrets are base64 encoded in etcd (kubectl get secret -o yaml)
- [ ] No secrets visible in plaintext in logs
- [ ] Environment variables properly injected into pods

### User Story 4 - AI-Assisted Operations ✅

- [ ] kubectl-ai installed and functional
- [ ] kagent installed and functional
- [ ] 5+ kubectl-ai command examples documented and verified
- [ ] kagent health check script functional
- [ ] Docker AI usage documented for vulnerability scanning

### User Story 5 - One-Command Deployment Experience ✅

- [ ] `./scripts/k8s/deploy.sh` completes successfully from clean state
- [ ] Deployment completes in under 10 minutes
- [ ] Script checks prerequisites and provides clear errors
- [ ] Script displays access URLs at completion
- [ ] `./scripts/k8s/verify.sh` validates deployment
- [ ] `./scripts/k8s/test.sh` runs automated acceptance tests

### Final Acceptance ✅

- [ ] All 5 user stories independently testable
- [ ] No Phase 3 application code modified (only added health endpoint)
- [ ] Comprehensive documentation complete
- [ ] Production readiness gaps documented
- [ ] Known issues and troubleshooting documented

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- US1 BLOCKS US2, US3 - must complete deployment before health checks/config
- US4 is independent and can run in parallel with US2/US3
- US5 should be last - it automates all previous stories
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Infrastructure testing uses "deploy-verify" workflow, not unit tests
- Avoid: modifying Phase 3 code (except adding frontend health endpoint)
