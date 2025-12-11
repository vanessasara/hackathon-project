# Quickstart: Cloud Deployment to DigitalOcean

**Feature**: 005-cloud-deployment
**Date**: 2025-12-04
**Estimated Time**: 30-45 minutes (first deployment)

## Prerequisites

### 1. DigitalOcean Account
- Sign up at [digitalocean.com](https://www.digitalocean.com)
- Add payment method (will charge ~$24/month)

### 2. Local Tools
```bash
# Install doctl (DigitalOcean CLI)
# Ubuntu/WSL
sudo snap install doctl

# macOS
brew install doctl

# Verify installation
doctl version
```

### 3. GitHub Repository
- Repository must be on GitHub
- Admin access to configure secrets

---

## Step 1: Create DigitalOcean Resources

### 1.1 Authenticate doctl
```bash
# Get API token from DO dashboard: API > Generate New Token
doctl auth init
# Paste your token when prompted
```

### 1.2 Create Kubernetes Cluster
```bash
doctl kubernetes cluster create todo-app-cluster \
  --region nyc1 \
  --node-pool "name=default;size=s-2vcpu-4gb;count=1" \
  --wait

# Save kubeconfig
doctl kubernetes cluster kubeconfig save todo-app-cluster

# Verify connection
kubectl get nodes
```

### 1.3 Create Container Registry
```bash
# Create registry (free tier)
doctl registry create todo-app-registry

# Connect registry to cluster
doctl registry kubernetes-manifest | kubectl apply -f -

# Login to registry
doctl registry login
```

---

## Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DIGITALOCEAN_ACCESS_TOKEN` | Your DO API token |
| `DATABASE_URL` | Your Neon PostgreSQL URL |
| `BETTER_AUTH_SECRET` | Your auth secret |
| `OPENAI_API_KEY` | Your OpenAI API key |

---

## Step 3: Deploy (Automated)

### Push to main branch
```bash
git checkout main
git merge 005-cloud-deployment
git push origin main
```

GitHub Actions will automatically:
1. Build Docker images
2. Push to DO Container Registry
3. Deploy to DOKS cluster

### Monitor deployment
```bash
# Watch GitHub Actions progress
# Go to: https://github.com/<owner>/<repo>/actions

# Or check pods directly
kubectl get pods -w
```

---

## Step 4: Access Application

### Get Node IP
```bash
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
echo "App URL: http://$NODE_IP:30080"
```

### Verify
```bash
# Test frontend
curl http://$NODE_IP:30080

# Open in browser
open http://$NODE_IP:30080
```

---

## Manual Deployment (Alternative)

If you prefer manual deployment without CI/CD:

```bash
cd phase-5-cloud

# Build and push images
docker build -t registry.digitalocean.com/todo-app-registry/backend:latest ./backend
docker build -t registry.digitalocean.com/todo-app-registry/frontend:latest ./frontend
docker push registry.digitalocean.com/todo-app-registry/backend:latest
docker push registry.digitalocean.com/todo-app-registry/frontend:latest

# Deploy with Helm
helm upgrade --install todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-doks.yaml \
  --set secrets.DATABASE_URL=$DATABASE_URL \
  --set secrets.BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET \
  --set secrets.OPENAI_API_KEY=$OPENAI_API_KEY
```

---

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Image pull errors
```bash
# Verify registry connection
kubectl get secret -o name | grep registry
doctl registry kubernetes-manifest | kubectl apply -f -
```

### Can't access application
```bash
# Check service
kubectl get svc

# Check node external IP
kubectl get nodes -o wide

# Verify NodePort is exposed
kubectl describe svc todo-app-frontend
```

### Cost monitoring
```bash
# Check current resources
doctl kubernetes cluster list
doctl compute droplet list
doctl registry get

# Estimated cost: ~$24/month
# - 1 node (s-2vcpu-4gb): $24
# - Registry (free tier): $0
# - No LoadBalancer: $0
```

---

## Cleanup

To remove all resources and stop charges:

```bash
# Delete cluster
doctl kubernetes cluster delete todo-app-cluster --force

# Delete registry
doctl registry delete --force

# Verify deletion
doctl kubernetes cluster list
doctl registry get
```

---

## Quick Reference

| Item | Value |
|------|-------|
| Cluster Name | todo-app-cluster |
| Region | nyc1 |
| Node Size | s-2vcpu-4gb |
| Monthly Cost | ~$24 |
| App URL | http://<NODE_IP>:30080 |
| Registry | registry.digitalocean.com/todo-app-registry |
