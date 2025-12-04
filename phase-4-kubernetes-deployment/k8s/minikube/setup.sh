#!/bin/bash
# Minikube Cluster Setup Script
# Purpose: Initialize a Minikube cluster with appropriate resources for the Todo App

set -e  # Exit on error

echo "=== Minikube Cluster Setup ==="

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Error: Minikube is not installed"
    echo "Install Minikube: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if Minikube is already running
if minikube status | grep -q "Running"; then
    echo "⚠️  Minikube is already running"
    read -p "Do you want to delete and recreate the cluster? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Deleting existing cluster..."
        minikube delete
    else
        echo "✅ Using existing cluster"
        exit 0
    fi
fi

# Start Minikube with specified resources
echo "🚀 Starting Minikube cluster..."
minikube start \
    --cpus=4 \
    --memory=8192 \
    --disk-size=20g \
    --driver=docker \
    --kubernetes-version=v1.28.0

# Enable required addons
echo "📦 Enabling Minikube addons..."
minikube addons enable metrics-server
minikube addons enable ingress

# Create namespace for the application
echo "🔧 Creating namespace 'todo-app'..."
kubectl create namespace todo-app || echo "⚠️  Namespace 'todo-app' already exists"

# Set default namespace
echo "🔧 Setting default namespace to 'todo-app'..."
kubectl config set-context --current --namespace=todo-app

# Display cluster info
echo ""
echo "✅ Minikube cluster setup complete!"
echo ""
echo "📊 Cluster Information:"
kubectl cluster-info
echo ""
echo "🌐 Minikube IP: $(minikube ip)"
echo "📁 Default namespace: todo-app"
echo ""
echo "Next steps:"
echo "  1. Run: ./k8s/minikube/build-images.sh (build Docker images)"
echo "  2. Run: ./scripts/k8s/deploy.sh (deploy application)"
