#!/bin/bash
# One-Command Deployment Script
# Purpose: Complete deployment workflow from source to running application

set -e  # Exit on error

echo "=== Todo App Kubernetes Deployment ==="
echo ""

# Get project root directory (assuming script is in scripts/k8s/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Step 1: Check Prerequisites
echo "Step 1/7: Checking prerequisites..."
MISSING_TOOLS=()

if ! command -v docker &> /dev/null; then
    MISSING_TOOLS+=("docker")
fi
if ! command -v minikube &> /dev/null; then
    MISSING_TOOLS+=("minikube")
fi
if ! command -v helm &> /dev/null; then
    MISSING_TOOLS+=("helm")
fi
if ! command -v kubectl &> /dev/null; then
    MISSING_TOOLS+=("kubectl")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    log_error "Missing required tools: ${MISSING_TOOLS[*]}"
    echo ""
    echo "Install missing tools:"
    echo "  - Docker: https://docs.docker.com/get-docker/"
    echo "  - Minikube: https://minikube.sigs.k8s.io/docs/start/"
    echo "  - Helm: https://helm.sh/docs/intro/install/"
    echo "  - kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi
log_info "All prerequisites installed"

# Step 2: Check Minikube Status
echo ""
echo "Step 2/7: Checking Minikube cluster..."
if ! minikube status | grep -q "Running"; then
    log_warn "Minikube is not running. Starting Minikube..."
    ./k8s/minikube/setup.sh
else
    log_info "Minikube is running"
fi

# Step 3: Build Docker Images
echo ""
echo "Step 3/7: Building Docker images..."
./k8s/minikube/build-images.sh

# Step 4: Create Namespace
echo ""
echo "Step 4/7: Creating namespace..."
if kubectl get namespace todo-app &> /dev/null; then
    log_info "Namespace 'todo-app' already exists"
else
    kubectl create namespace todo-app
    log_info "Namespace 'todo-app' created"
fi

# Step 5: Load Secrets from .env
echo ""
echo "Step 5/7: Loading secrets from .env file..."
if [ ! -f ".env" ]; then
    log_error ".env file not found!"
    echo ""
    echo "Create a .env file with the following variables:"
    echo "  DATABASE_URL=postgresql://..."
    echo "  BETTER_AUTH_SECRET=your-secret-min-32-chars"
    echo "  OPENAI_API_KEY=sk-..."
    echo "  CLOUDFLARE_R2_ACCOUNT_ID=..."
    echo "  CLOUDFLARE_R2_ACCESS_KEY_ID=..."
    echo "  CLOUDFLARE_R2_SECRET_ACCESS_KEY=..."
    echo "  CLOUDFLARE_R2_BUCKET_NAME=..."
    exit 1
fi

# Source .env file
set -a  # Export all variables
source .env
set +a

# Validate required secrets
if [ -z "$DATABASE_URL" ]; then
    log_error "DATABASE_URL is required in .env"
    exit 1
fi
if [ -z "$BETTER_AUTH_SECRET" ]; then
    log_error "BETTER_AUTH_SECRET is required in .env"
    exit 1
fi
if [ -z "$OPENAI_API_KEY" ]; then
    log_error "OPENAI_API_KEY is required in .env"
    exit 1
fi

log_info "Secrets loaded from .env"

# Step 6: Deploy with Helm
echo ""
echo "Step 6/7: Deploying application with Helm..."
RELEASE_NAME="todo-app"

# Check if release exists
if helm list -n todo-app | grep -q "$RELEASE_NAME"; then
    log_warn "Helm release '$RELEASE_NAME' exists. Upgrading..."
    helm upgrade "$RELEASE_NAME" ./helm/todo-app \
        -f ./helm/todo-app/values-dev.yaml \
        -n todo-app \
        --set secrets.DATABASE_URL="$DATABASE_URL" \
        --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
        --set secrets.OPENAI_API_KEY="$OPENAI_API_KEY" \
        --set secrets.CLOUDFLARE_R2_ACCOUNT_ID="${CLOUDFLARE_R2_ACCOUNT_ID:-}" \
        --set secrets.CLOUDFLARE_R2_ACCESS_KEY_ID="${CLOUDFLARE_R2_ACCESS_KEY_ID:-}" \
        --set secrets.CLOUDFLARE_R2_SECRET_ACCESS_KEY="${CLOUDFLARE_R2_SECRET_ACCESS_KEY:-}" \
        --set secrets.CLOUDFLARE_R2_BUCKET_NAME="${CLOUDFLARE_R2_BUCKET_NAME:-}" \
        --wait --timeout=5m
    log_info "Helm release upgraded"
else
    log_info "Installing new Helm release..."
    helm install "$RELEASE_NAME" ./helm/todo-app \
        -f ./helm/todo-app/values-dev.yaml \
        -n todo-app \
        --set secrets.DATABASE_URL="$DATABASE_URL" \
        --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
        --set secrets.OPENAI_API_KEY="$OPENAI_API_KEY" \
        --set secrets.CLOUDFLARE_R2_ACCOUNT_ID="${CLOUDFLARE_R2_ACCOUNT_ID:-}" \
        --set secrets.CLOUDFLARE_R2_ACCESS_KEY_ID="${CLOUDFLARE_R2_ACCESS_KEY_ID:-}" \
        --set secrets.CLOUDFLARE_R2_SECRET_ACCESS_KEY="${CLOUDFLARE_R2_SECRET_ACCESS_KEY:-}" \
        --set secrets.CLOUDFLARE_R2_BUCKET_NAME="${CLOUDFLARE_R2_BUCKET_NAME:-}" \
        --wait --timeout=5m
    log_info "Helm release installed"
fi

# Step 7: Verify Deployment
echo ""
echo "Step 7/7: Verifying deployment..."
echo ""
echo "Waiting for pods to be ready (max 2 minutes)..."

TIMEOUT=120
ELAPSED=0
INTERVAL=5

while [ $ELAPSED -lt $TIMEOUT ]; do
    READY_PODS=$(kubectl get pods -n todo-app -o jsonpath='{.items[*].status.containerStatuses[*].ready}' | grep -o "true" | wc -l || echo "0")
    TOTAL_PODS=$(kubectl get pods -n todo-app --no-headers | wc -l)

    echo "  Ready: $READY_PODS/$TOTAL_PODS pods"

    if [ "$READY_PODS" -eq "$TOTAL_PODS" ] && [ "$TOTAL_PODS" -gt 0 ]; then
        log_info "All pods are ready!"
        break
    fi

    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
done

if [ $ELAPSED -ge $TIMEOUT ]; then
    log_warn "Timeout waiting for pods. Check status with: kubectl get pods -n todo-app"
fi

# Display access information
echo ""
echo "========================================="
echo "          DEPLOYMENT COMPLETE"
echo "========================================="
echo ""
MINIKUBE_IP=$(minikube ip)
echo "🌐 Frontend URL: http://$MINIKUBE_IP:30300"
echo ""
echo "📊 Pod Status:"
kubectl get pods -n todo-app
echo ""
echo "🔍 Service Status:"
kubectl get services -n todo-app
echo ""
echo "Useful commands:"
echo "  - View logs (frontend): kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f"
echo "  - View logs (backend):  kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f"
echo "  - Shell into pod:       kubectl exec -n todo-app -it <pod-name> -- /bin/sh"
echo "  - Restart deployment:   kubectl rollout restart -n todo-app deployment/todo-app-frontend"
echo "  - Delete deployment:    helm uninstall todo-app -n todo-app"
echo ""
