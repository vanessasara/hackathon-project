# ADR-0003: NodePort Service Exposure for Development Environment

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-04
- **Feature:** 004-kubernetes-deployment
- **Context:** Phase 4 requires exposing the frontend service externally for browser access on Minikube. Must decide on Kubernetes service exposure strategy for development. Backend remains internal (ClusterIP only). Production (Phase 5) will likely use Ingress with TLS.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects access patterns, security posture, production migration path
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - NodePort vs Ingress vs LoadBalancer
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects all external access, DNS, security, documentation
-->

## Decision

**Use NodePort service type for frontend on port 30300, keep backend as ClusterIP for development on Minikube. Document Ingress setup for production readiness.**

**Service Configuration**:
- **Frontend Service**: `type: NodePort`, `port: 3000`, `nodePort: 30300`
  - External access: `http://$(minikube ip):30300`
- **Backend Service**: `type: ClusterIP`, `port: 8000`
  - Internal access only: `http://backend-service:8000`
- **Service Discovery**: Kubernetes DNS for internal communication
- **Production Note**: Document Ingress transition path in `docs/kubernetes/DEPLOYMENT.md`

**Rationale**: NodePort is simplest for Minikube development (no additional setup), provides immediate external access, works reliably on all platforms (Windows/Linux/macOS), and scales to production with minimal chart changes (just update service type and add Ingress).

## Consequences

### Positive

- **Zero Setup**: Works immediately after Helm install
- **No Additional Components**: No Ingress controller required
- **Platform Agnostic**: Works on Windows, Linux, macOS consistently
- **Simple Access**: Direct IP:Port access, no DNS configuration
- **Debug Friendly**: Easy to curl, test, troubleshoot
- **Port Predictable**: Fixed NodePort 30300 (not random high port)
- **Documentation**: Clear, simple access instructions for users

### Negative

- **Non-Production Pattern**: Production uses Ingress, not NodePort
- **No DNS**: Access via IP address, not friendly domain names
- **No TLS**: HTTP only, no built-in HTTPS support
- **Port Range Limitations**: NodePort restricted to 30000-32767
- **Firewall Considerations**: May require firewall rules in some environments
- **Single Entry Point**: No load balancing across multiple frontend replicas (not an issue with 1 replica in dev)

**Mitigation**:
- Document production Ingress setup in `docs/kubernetes/DEPLOYMENT.md`
- Provide Ingress example configuration for Phase 5 migration
- Note TLS setup requirements for production
- Explain transition path from NodePort → Ingress

## Alternatives Considered

### Alternative 1: Ingress with NGINX Ingress Controller

**Strategy**: Deploy Ingress controller, create Ingress resource with hostname routing

**Pros**:
- Production-like setup
- DNS-based access (e.g., `todo-app.local`)
- TLS termination possible
- Path-based routing (frontend + backend on same domain)
- Load balancing built-in
- Industry standard pattern

**Cons**:
- Requires `minikube addons enable ingress`
- Requires `minikube tunnel` running in background for access
- DNS configuration (hosts file editing) for local domains
- Additional complexity to debug (Ingress + Service + Deployment)
- Slower startup (Ingress controller pod deployment)
- Platform-specific issues (Windows Docker Desktop, WSL2 networking)

**Why Rejected**: Over-engineered for Phase 4 development. Ingress benefits (DNS, TLS, path routing) not needed for local testing. Added complexity slows down MVP delivery. Better as optional production readiness enhancement.

### Alternative 2: LoadBalancer Service Type

**Strategy**: Set service type to LoadBalancer

**Pros**:
- Most production-like (cloud providers use LoadBalancer)
- Automatic external IP assignment (in cloud)
- Clean service configuration

**Cons**:
- Requires MetalLB or similar load balancer in Minikube
- Extra setup: `minikube addons enable metallb`, IP range configuration
- Adds unnecessary component for single-service access
- More moving parts to troubleshoot
- Overkill for development environment

**Why Rejected**: LoadBalancer designed for cloud providers (AWS ELB, GCP LB). In Minikube, requires MetalLB addon, which adds complexity without benefit over NodePort for dev.

### Alternative 3: Port Forwarding (kubectl port-forward)

**Strategy**: Use `kubectl port-forward deployment/frontend 3000:3000`

**Pros**:
- No service configuration changes needed
- Direct pod access
- Simplest possible approach
- No NodePort range limitations

**Cons**:
- Manual step after every deployment
- Connection dies if pod restarts
- Cannot access from other machines (localhost only)
- Not suitable for team demos or testing
- Requires terminal session to stay open
- Inconvenient for automated testing

**Why Rejected**: Manual and fragile. NodePort provides persistent, automatic access without manual intervention. Port forwarding better for quick debugging, not primary access method.

### Alternative 4: ClusterIP with Minikube Tunnel

**Strategy**: Use ClusterIP service type, run `minikube tunnel` for external access

**Pros**:
- More production-like (ClusterIP standard in cloud with Ingress)
- Services accessible on cluster IPs
- Cleaner service configuration

**Cons**:
- Requires `minikube tunnel` running in background
- Needs sudo/admin privileges on some systems
- Platform-specific issues (Windows, WSL2)
- Connection breaks if tunnel stops
- More complex documentation ("Run tunnel, then access...")

**Why Rejected**: Minikube tunnel adds operational overhead and platform compatibility issues. NodePort works reliably everywhere without background processes.

## References

- Feature Spec: [specs/004-kubernetes-deployment/spec.md](../../specs/004-kubernetes-deployment/spec.md)
- Implementation Plan: [specs/004-kubernetes-deployment/plan.md](../../specs/004-kubernetes-deployment/plan.md#adr-003-nodeport-vs-ingress-for-frontend-exposure)
- Related ADRs: ADR-0001 (Helm chart configures service types)
- Kubernetes Service Types: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types
- Ingress Migration Path: [docs/kubernetes/DEPLOYMENT.md](../../docs/kubernetes/DEPLOYMENT.md) (to be created in implementation)
- Evaluator Evidence: [PHR-0001](../prompts/004-kubernetes-deployment/0001-phase-4-kubernetes-deployment-planning.plan.prompt.md)
