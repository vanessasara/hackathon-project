#!/bin/bash
# Minikube Image Build Script
# Purpose: Build Docker images directly in Minikube's Docker daemon

set -e  # Exit on error

echo "=== Building Docker Images in Minikube ==="

# Check if Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "❌ Error: Minikube is not running"
    echo "Start Minikube first: ./k8s/minikube/setup.sh"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    exit 1
fi

# Get project root directory (assuming script is in k8s/minikube/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "📁 Project root: $PROJECT_ROOT"

# Set Docker environment to use Minikube's Docker daemon
echo "🔧 Switching Docker context to Minikube..."
eval $(minikube docker-env)

# Build Frontend Image
echo ""
echo "🏗️  Building Frontend Image (todo-frontend:latest)..."
docker build \
    -t todo-frontend:latest \
    -f "$PROJECT_ROOT/frontend/Dockerfile" \
    "$PROJECT_ROOT/frontend/"

# Build Backend Image
echo ""
echo "🏗️  Building Backend Image (todo-backend:latest)..."
docker build \
    -t todo-backend:latest \
    -f "$PROJECT_ROOT/backend/Dockerfile" \
    "$PROJECT_ROOT/backend/"

# Verify images were built
echo ""
echo "✅ Images built successfully!"
echo ""
echo "📦 Available images:"
docker images | grep -E "^(REPOSITORY|todo-)" || echo "⚠️  No images found"

echo ""
echo "Next steps:"
echo "  1. Ensure .env file exists with required secrets"
echo "  2. Run: ./scripts/k8s/deploy.sh (deploy application)"
echo ""
echo "💡 Note: Images are built in Minikube's Docker daemon"
echo "   They won't appear in your host's Docker image list"
