# ADR-0002: Minikube Docker Daemon for Local Development

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-04
- **Feature:** 004-kubernetes-deployment
- **Context:** Phase 4 requires building Docker images for frontend and backend, then deploying them to Minikube. Must decide on image registry strategy for development workflow. Production (Phase 5) will use cloud registries, but local development needs different approach.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects build workflow, image availability, CI/CD pipeline evolution
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Minikube daemon vs Docker Hub vs Local registry
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects all developers, build scripts, deployment process
-->

## Decision

**Build Docker images directly in Minikube's Docker daemon using `eval $(minikube docker-env)` and set `imagePullPolicy: Never` in Helm deployments.**

**Build Strategy**:
- **Image Building**: Run `docker build` after setting Minikube Docker context
- **Image Names**: `todo-frontend:latest` and `todo-backend:latest`
- **Pull Policy**: `imagePullPolicy: Never` in Deployment manifests
- **Rebuild Workflow**: Re-run `eval $(minikube docker-env)` → `docker build` → `kubectl rollout restart`
- **Script Automation**: `k8s/minikube/build-images.sh` handles context switching

**Rationale**: Zero setup overhead, fast iteration (no registry push/pull), images stay local to Minikube, perfect for development. Production migration (Phase 5) simply changes image names and pull policy.

## Consequences

### Positive

- **Zero Setup**: No registry configuration or credentials needed
- **Fast Iteration**: `docker build` → `helm upgrade` in seconds (no push/pull)
- **No Network Overhead**: Images never leave local machine
- **Cost**: Free (no registry hosting fees)
- **Simplicity**: Minimal moving parts, easy to debug
- **Local Isolation**: Images don't pollute external registries
- **Fast Startup**: No image pull delays (images already in daemon)

### Negative

- **Minikube-Specific**: Does not work with other K8s distributions (kind, k3s, cloud)
- **Non-Persistent**: Images lost if Minikube deleted (minikube delete)
- **Developer Context**: Must remember to set Docker context (easy to forget)
- **Team Sharing**: Cannot share images with team (each developer builds locally)
- **Production Divergence**: Different workflow than production (images vs registry)
- **CI/CD Gap**: Build pipeline will differ from local development

**Mitigation**: Phase 5 cloud deployment will use proper registry (ECR, GCR, ACR). Document transition path in production readiness notes.

## Alternatives Considered

### Alternative 1: Docker Hub Public Registry

**Strategy**: Push images to Docker Hub, pull in Minikube

**Pros**:
- Industry standard workflow
- Team can share images
- Same workflow as production
- Works across K8s distributions
- Images persist beyond Minikube lifecycle

**Cons**:
- Requires Docker Hub account setup
- Slow iteration (build → push → pull → deploy)
- Network dependency for local development
- Registry quotas and rate limits
- Public images (privacy concern for enterprise)
- Credentials management overhead

**Why Rejected**: Adds unnecessary complexity and latency to local development. Benefit (team sharing) not needed for single-developer Phase 4 work.

### Alternative 2: Local Registry in Minikube

**Strategy**: Run registry container in Minikube, push images there

**Pros**:
- More production-like workflow
- Images persist in Minikube
- No external dependencies
- Team can share images (if network accessible)
- Works with other local K8s setups

**Cons**:
- Requires registry deployment (extra complexity)
- Push/pull overhead (slower than direct daemon)
- Port forwarding or ingress setup for access
- Storage management in Minikube
- More moving parts to debug

**Why Rejected**: Over-engineered for local development. Adds complexity without meaningful benefit over Docker daemon approach.

### Alternative 3: GitHub Container Registry (GHCR)

**Strategy**: Push images to GitHub Packages, pull in Minikube

**Pros**:
- Integrated with GitHub repository
- Private images with repo permissions
- Free for public repos
- Good for CI/CD pipelines
- Team collaboration support

**Cons**:
- GitHub PAT setup required
- Push/pull latency on every build
- Network dependency
- GHCR quotas and limits
- Authentication complexity
- Slower local development loop

**Why Rejected**: Same issues as Docker Hub. Better suited for CI/CD and production, not local development iteration.

### Alternative 4: Kind (Kubernetes in Docker) with Kind Load

**Strategy**: Use kind instead of Minikube, load images with `kind load docker-image`

**Pros**:
- Similar to Minikube daemon approach
- Lighter weight than Minikube
- Better CI/CD integration
- Faster cluster startup

**Cons**:
- Requires switching from Minikube (project requirement specifies Minikube)
- Different setup commands
- Less mature addons ecosystem
- Phase 4 requirements explicitly require Minikube

**Why Rejected**: Phase 4 hackathon requirements explicitly mandate Minikube. Cannot deviate from requirement.

## References

- Feature Spec: [specs/004-kubernetes-deployment/spec.md](../../specs/004-kubernetes-deployment/spec.md)
- Implementation Plan: [specs/004-kubernetes-deployment/plan.md](../../specs/004-kubernetes-deployment/plan.md#adr-002-minikube-docker-daemon-vs-external-registry)
- Related ADRs: ADR-0001 (Helm chart affects imagePullPolicy configuration)
- Minikube Docker Env Docs: https://minikube.sigs.k8s.io/docs/handbook/pushing/#1-pushing-directly-to-the-in-cluster-docker-daemon-docker-env
- Evaluator Evidence: [PHR-0001](../prompts/004-kubernetes-deployment/0001-phase-4-kubernetes-deployment-planning.plan.prompt.md)
