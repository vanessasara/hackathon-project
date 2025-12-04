# ADR-0001: Monolithic Helm Chart for Multi-Service Deployment

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-04
- **Feature:** 004-kubernetes-deployment
- **Context:** Phase 4 requires deploying Phase 3 Todo Chatbot (Next.js frontend + FastAPI backend) to Minikube using Helm charts. Must decide on Helm chart structure strategy for managing multiple related services.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects deployment architecture, maintainability, scalability to cloud
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Monolithic vs Umbrella vs Raw manifests
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects all services, future deployments, team workflows
-->

## Decision

**Use a single monolithic Helm chart (`helm/todo-app/`) with modular template organization for deploying both frontend and backend services.**

**Chart Structure**:
- **Chart Metadata**: Single `Chart.yaml` (v1.0.0, app v3.0.0)
- **Template Organization**: Modular subdirectories for clarity
  - `templates/frontend/` - Frontend Deployment and Service
  - `templates/backend/` - Backend Deployment and Service
  - `templates/shared/` - ConfigMap and Secret shared by both services
  - `templates/_helpers.tpl` - Shared template functions (labels, selectors)
- **Configuration**: Single `values.yaml` with sections for each service
- **Environment Overrides**: `values-dev.yaml` for Minikube-specific settings

**Rationale**: Simplifies deployment, enables shared configuration (ConfigMap, Secret), provides single source of truth for the entire application stack, and scales naturally to cloud Kubernetes with minimal changes.

## Consequences

### Positive

- **Simplified Deployment**: Single `helm install` command deploys entire stack
- **Shared Configuration**: ConfigMap and Secret naturally shared across services
- **Atomic Operations**: Updates, rollbacks affect all services together
- **Service Discovery**: Services easily reference each other via stable names
- **Reduced Boilerplate**: Shared helpers, common labels, consistent patterns
- **Developer Experience**: Easier to understand, test, and iterate locally
- **Cloud Migration**: Chart structure scales to production (just update values)
- **Dependency Management**: Service startup order and dependencies handled in one place

### Negative

- **Coupling**: Services deployed together, cannot version independently
- **Blast Radius**: Issue in one template can affect entire deployment
- **Release Coordination**: Cannot deploy frontend without backend (atomic releases)
- **Chart Complexity**: Single chart grows with more services (manageable for 2 services)
- **Testing Granularity**: Cannot test service deployments in isolation
- **Team Boundaries**: Less clear ownership if teams split by service

**Mitigation**: For Phase 5 (cloud deployment), can split into separate charts if team/service boundaries require it. Current 2-service setup benefits from monolithic approach.

## Alternatives Considered

### Alternative 1: Umbrella Chart (Chart of Charts)

**Structure**: Parent chart (`charts/`) with `frontend/` and `backend/` as dependencies

**Pros**:
- Independent versioning of frontend and backend
- Clear service boundaries and ownership
- Can deploy services separately
- Better for large teams with service ownership

**Cons**:
- More complex structure (3 charts vs 1)
- Shared configuration requires parent chart coordination
- Service discovery more complex (different release names)
- Overhead for 2-service application
- More boilerplate (3x Chart.yaml, values.yaml)

**Why Rejected**: Over-engineered for 2 tightly-coupled services. Umbrella charts benefit large microservice ecosystems (5+ services), not our 2-service monolith.

### Alternative 2: Raw Kubernetes Manifests

**Structure**: Individual YAML files in `k8s/` directory

**Pros**:
- No Helm dependency
- Direct, explicit configuration
- Simpler for small deployments
- No templating to learn

**Cons**:
- No templating or parameterization
- Duplication of values across manifests
- No release management or rollbacks
- Cannot override values for environments (dev, prod)
- Manual secret management
- No versioning of deployments

**Why Rejected**: Loses all benefits of Helm (templating, versioning, rollbacks, environment overrides). Phase 5 cloud deployment would require complete rewrite.

### Alternative 3: Kustomize

**Structure**: Base manifests with overlays for environments

**Pros**:
- Native Kubernetes tool
- Template-free (uses patching)
- Good for configuration variations

**Cons**:
- Less expressive than Helm templates
- No release history or easy rollbacks
- Secrets management less mature
- Less community adoption for complex apps
- Learning curve for patch-based approach

**Why Rejected**: Helm provides richer templating, better release management, and wider industry adoption. Kustomize better for simpler use cases.

## References

- Feature Spec: [specs/004-kubernetes-deployment/spec.md](../../specs/004-kubernetes-deployment/spec.md)
- Implementation Plan: [specs/004-kubernetes-deployment/plan.md](../../specs/004-kubernetes-deployment/plan.md#adr-001-monolithic-helm-chart-vs-umbrella-chart)
- Related ADRs: None (first ADR for this feature)
- Helm Best Practices: https://helm.sh/docs/chart_best_practices/
- Evaluator Evidence: [PHR-0001](../prompts/004-kubernetes-deployment/0001-phase-4-kubernetes-deployment-planning.plan.prompt.md)
