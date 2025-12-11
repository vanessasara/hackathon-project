# Kubernetes Deployment - Quick Start

This directory contains Kubernetes deployment resources for the Todo App.

## Prerequisites

- Docker 24+
- Minikube 1.32+
- Helm 3.x
- kubectl 1.28+

## Quick Deployment

### 1. One-Command Deployment

```bash
./scripts/k8s/deploy.sh
```

This script will:
- Check prerequisites
- Start Minikube (if not running)
- Build Docker images
- Deploy with Helm
- Wait for pods to be ready
- Display access URLs

### 2. Manual Step-by-Step

#### a. Start Minikube

```bash
./k8s/minikube/setup.sh
```

#### b. Build Images

```bash
./k8s/minikube/build-images.sh
```

#### c. Create .env File

```bash
# Copy and edit with your values
cp .env.example .env
```

Required variables:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Min 32 characters
- `OPENAI_API_KEY` - OpenAI API key (sk-...)

Optional (for image uploads):
- `CLOUDFLARE_R2_ACCOUNT_ID`
- `CLOUDFLARE_R2_ACCESS_KEY_ID`
- `CLOUDFLARE_R2_SECRET_ACCESS_KEY`
- `CLOUDFLARE_R2_BUCKET_NAME`

#### d. Deploy with Helm

```bash
source .env  # Load secrets

helm install todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-dev.yaml \
  -n todo-app \
  --create-namespace \
  --set secrets.DATABASE_URL="$DATABASE_URL" \
  --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --set secrets.OPENAI_API_KEY="$OPENAI_API_KEY" \
  --wait
```

#### e. Access the Application

```bash
minikube ip  # Get cluster IP
# Then open: http://<minikube-ip>:30300
```

## Common Operations

### View Pod Status

```bash
kubectl get pods -n todo-app
```

### View Logs

```bash
# Frontend logs
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f

# Backend logs
kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f
```

### Rebuild and Redeploy

```bash
# Rebuild images
./k8s/minikube/build-images.sh

# Restart deployments
kubectl rollout restart -n todo-app deployment/todo-app-frontend
kubectl rollout restart -n todo-app deployment/todo-app-backend
```

### Cleanup

```bash
# Remove deployment
helm uninstall todo-app -n todo-app

# Or delete entire cluster
./k8s/minikube/cleanup.sh
```

## Directory Structure

```
k8s/
├── README.md              # This file
├── minikube/
│   ├── setup.sh          # Initialize Minikube cluster
│   ├── build-images.sh   # Build Docker images
│   └── cleanup.sh        # Teardown cluster
├── kubectl-ai/
│   └── examples.md       # kubectl-ai usage examples
└── kagent/
    └── health-check.sh   # Automated health checks
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pods -n todo-app

# Check logs
kubectl logs -n todo-app <pod-name>
```

### Image Pull Errors

Make sure images are built in Minikube's Docker daemon:

```bash
eval $(minikube docker-env)
docker images | grep todo-
```

### Port Already in Use

Check if another service is using port 30300:

```bash
lsof -i :30300
```

## Documentation

- [Deployment Guide](../docs/kubernetes/DEPLOYMENT.md) - Detailed step-by-step guide
- [Troubleshooting](../docs/kubernetes/TROUBLESHOOTING.md) - Common issues and solutions
- [AI DevOps Tools](../docs/kubernetes/AI_DEVOPS.md) - kubectl-ai, kagent, Docker AI usage

## Architecture

- **Frontend**: Next.js 16, exposed via NodePort 30300
- **Backend**: FastAPI, internal ClusterIP service
- **Database**: External Neon PostgreSQL
- **Storage**: External Cloudflare R2
- **Config**: ConfigMap (non-sensitive) + Secret (sensitive)
- **Health**: Readiness and Liveness probes on `/api/health`
