#!/bin/bash
# Minikube Cleanup Script
# Purpose: Teardown Minikube cluster and clean up resources

set -e  # Exit on error

echo "=== Minikube Cluster Cleanup ==="

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "⚠️  Minikube is not installed - nothing to clean up"
    exit 0
fi

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo "⚠️  Minikube is not running - nothing to clean up"
    exit 0
fi

# Confirm deletion
read -p "⚠️  This will delete the Minikube cluster and all data. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

# Delete Helm release if it exists
echo "🗑️  Checking for Helm releases..."
if command -v helm &> /dev/null; then
    if helm list -n todo-app 2>/dev/null | grep -q "todo-app"; then
        echo "🗑️  Uninstalling Helm release..."
        helm uninstall todo-app -n todo-app
    else
        echo "✓ No Helm releases found"
    fi
else
    echo "⚠️  Helm not installed, skipping Helm cleanup"
fi

# Delete namespace (this will delete all resources in it)
echo "🗑️  Deleting namespace 'todo-app'..."
kubectl delete namespace todo-app --ignore-not-found=true

# Stop and delete Minikube cluster
echo "🗑️  Stopping and deleting Minikube cluster..."
minikube stop
minikube delete

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "To recreate the cluster:"
echo "  ./k8s/minikube/setup.sh"
