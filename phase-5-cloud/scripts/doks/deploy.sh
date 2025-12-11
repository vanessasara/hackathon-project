#!/bin/bash
# Manual deployment script for DigitalOcean Kubernetes (DOKS)
#
# Prerequisites:
#   - doctl CLI installed and authenticated
#   - kubectl configured for DOKS cluster
#   - Docker installed
#   - Environment variables set: DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY
#
# Usage:
#   cd phase-5-cloud
#   ./scripts/doks/deploy.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== DOKS Deployment Script ===${NC}"

# Configuration
REGISTRY="registry.digitalocean.com/todoappregistry2024"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Check required environment variables
check_env() {
    local missing=0
    for var in DATABASE_URL BETTER_AUTH_SECRET OPENAI_API_KEY; do
        if [ -z "${!var}" ]; then
            echo -e "${RED}Error: $var is not set${NC}"
            missing=1
        fi
    done
    if [ $missing -eq 1 ]; then
        echo -e "${YELLOW}Tip: Source your .env file or export the variables${NC}"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"

    command -v doctl >/dev/null 2>&1 || { echo -e "${RED}doctl is required but not installed.${NC}"; exit 1; }
    command -v kubectl >/dev/null 2>&1 || { echo -e "${RED}kubectl is required but not installed.${NC}"; exit 1; }
    command -v docker >/dev/null 2>&1 || { echo -e "${RED}docker is required but not installed.${NC}"; exit 1; }
    command -v helm >/dev/null 2>&1 || { echo -e "${RED}helm is required but not installed.${NC}"; exit 1; }

    echo -e "${GREEN}All prerequisites met.${NC}"
}

# Login to DO registry
registry_login() {
    echo -e "${YELLOW}Logging into DigitalOcean Container Registry...${NC}"
    doctl registry login --expiry-seconds 3600
}

# Build and push images
build_and_push() {
    echo -e "${YELLOW}Building and pushing Docker images...${NC}"

    cd "$PROJECT_DIR"

    # Build backend
    echo -e "${YELLOW}Building backend image...${NC}"
    docker build -t "$REGISTRY/backend:latest" ./backend
    docker push "$REGISTRY/backend:latest"

    # Build frontend
    echo -e "${YELLOW}Building frontend image...${NC}"
    docker build -t "$REGISTRY/frontend:latest" ./frontend
    docker push "$REGISTRY/frontend:latest"

    echo -e "${GREEN}Images pushed successfully.${NC}"
}

# Deploy with Helm
deploy_helm() {
    echo -e "${YELLOW}Deploying with Helm...${NC}"

    cd "$PROJECT_DIR"

    helm upgrade --install todo-app ./helm/todo-app \
        -f ./helm/todo-app/values-doks.yaml \
        --set secrets.DATABASE_URL="$DATABASE_URL" \
        --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
        --set secrets.OPENAI_API_KEY="$OPENAI_API_KEY"

    echo -e "${GREEN}Helm deployment complete.${NC}"
}

# Get access URL
get_access_url() {
    echo -e "${YELLOW}Getting access URL...${NC}"

    # Wait for pods to be ready
    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app=todo-app-frontend --timeout=120s 2>/dev/null || true

    # Get node external IP
    NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')

    if [ -z "$NODE_IP" ]; then
        echo -e "${YELLOW}Could not get external IP. Checking node status...${NC}"
        kubectl get nodes -o wide
    else
        echo -e "${GREEN}==================================${NC}"
        echo -e "${GREEN}Application deployed successfully!${NC}"
        echo -e "${GREEN}Access URL: http://$NODE_IP:30080${NC}"
        echo -e "${GREEN}==================================${NC}"
    fi
}

# Show status
show_status() {
    echo -e "${YELLOW}Current deployment status:${NC}"
    kubectl get pods
    kubectl get svc
}

# Main
main() {
    check_prerequisites
    check_env
    registry_login
    build_and_push
    deploy_helm
    get_access_url
    show_status
}

# Run if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
