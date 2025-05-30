# 🚀 GitHub Actions Deployment to Azure AKS

This guide shows how to deploy your ChatBot AI to Azure AKS using GitHub Actions secrets instead of Azure Key Vault.

## 📋 Prerequisites

1. ✅ Azure Container Registry (ACR)
2. ✅ Azure Kubernetes Service (AKS) cluster
3. ✅ GitHub repository
4. ✅ AWS Bedrock credentials

## 🔐 Step 1: Set Up GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

### Azure Credentials
```
ACR_USERNAME = your-acr-username
ACR_PASSWORD = your-acr-password
AZURE_CREDENTIALS = {
  "clientId": "your-service-principal-client-id",
  "clientSecret": "your-service-principal-secret",
  "subscriptionId": "your-subscription-id",
  "tenantId": "your-tenant-id"
}
```

### AWS Bedrock Credentials
```
AWS_ACCESS_KEY = your-aws-access-key-here
AWS_SECRET_KEY = your-aws-secret-key-here
AWS_REGION = us-east-1
MODEL_ID = anthropic.claude-3-sonnet-20240229-v1:0
SYSTEM_PROMPT = your-hebrew-system-prompt-here
```

## 🔧 Step 2: Update GitHub Actions Workflow

Edit [`.github/workflows/deploy-to-aks.yml`](.github/workflows/deploy-to-aks.yml) and update these values:

```yaml
env:
  AZURE_CONTAINER_REGISTRY: your-acr-name  # Replace with your ACR name
  RESOURCE_GROUP: myResourceGroup          # Replace with your resource group
  CLUSTER_NAME: myAKSCluster              # Replace with your AKS cluster name.
```

## 🏗️ Step 3: Create Azure Service Principal

```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth

# Grant AKS permissions
az role assignment create \
  --assignee {service-principal-client-id} \
  --role "Azure Kubernetes Service Cluster User Role" \
  --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.ContainerService/managedClusters/{aks-cluster-name}
```

Copy the JSON output to your `AZURE_CREDENTIALS` GitHub secret.

## 🐳 Step 4: Application Files

### Main Application
- [`Asafiz-Ai-Simple.py`](Asafiz-Ai-Simple.py) - Simplified app using environment variables
- [`Dockerfile`](Dockerfile) - Container configuration
- [`requirements.txt`](requirements.txt) - Python dependencies

### Kubernetes Manifests
- [`k8s/deployment.yaml`](k8s/deployment.yaml) - Pod deployment configuration
- [`k8s/service.yaml`](k8s/service.yaml) - Load balancer service

## 🚀 Step 5: Deploy

### Automatic Deployment
Push to `main` or `master` branch:
```bash
git add .
git commit -m "Deploy ChatBot AI to AKS"
git push origin main
```

### Manual Deployment
Go to GitHub → **Actions** → **Deploy to Azure AKS** → **Run workflow**

## 📊 Step 6: Monitor Deployment

### GitHub Actions
- Check the workflow run in GitHub Actions tab
- View logs for each step
- Monitor build and deployment status

### Kubernetes
```bash
# Get AKS credentials
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# Check deployment status
kubectl get pods -n chatbot-ai
kubectl get services -n chatbot-ai
kubectl logs -f deployment/chatbot-ai -n chatbot-ai

# Get external IP
kubectl get service chatbot-ai-service -n chatbot-ai
```

## 🔍 Step 7: Test Your Application

### Health Check
```bash
# Port forward for testing
kubectl port-forward service/chatbot-ai-service 8080:80 -n chatbot-ai

# Test health endpoint
curl http://localhost:8080/health
```

### Access Application
Once deployed, get the external IP:
```bash
kubectl get service chatbot-ai-service -n chatbot-ai
```

Visit `http://EXTERNAL-IP` in your browser.

## 🛠️ Troubleshooting

### Common Issues

1. **Image Pull Errors**
   ```bash
   # Check ACR credentials
   az acr login --name your-acr-name
   
   # Verify image exists
   az acr repository list --name your-acr-name
   ```

2. **Pod Startup Issues**
   ```bash
   # Check pod logs
   kubectl describe pod -l app=chatbot-ai -n chatbot-ai
   kubectl logs -l app=chatbot-ai -n chatbot-ai
   ```

3. **AWS Bedrock Connection Issues**
   ```bash
   # Check secrets
   kubectl get secret aws-bedrock-secrets -n chatbot-ai -o yaml
   
   # Test from pod
   kubectl exec -it deployment/chatbot-ai -n chatbot-ai -- python -c "
   import os
   print('AWS_ACCESS_KEY:', os.getenv('AWS_ACCESS_KEY')[:10] + '...')
   print('AWS_REGION:', os.getenv('AWS_REGION'))
   "
   ```

## 🔐 Security Benefits

✅ **Secrets in GitHub**: Encrypted and managed by GitHub  
✅ **No hardcoded credentials**: Environment variables only  
✅ **Automated deployment**: CI/CD pipeline  
✅ **Container security**: Non-root user, health checks  
✅ **Kubernetes security**: Resource limits, probes  

## 📁 File Structure

```
your-repo/
├── .github/workflows/
│   └── deploy-to-aks.yml          # GitHub Actions workflow
├── k8s/
│   ├── deployment.yaml            # Kubernetes deployment
│   └── service.yaml               # Kubernetes service
├── Asafiz-Ai-Simple.py           # Main application (env vars)
├── Dockerfile                     # Container configuration
├── requirements.txt               # Python dependencies
└── GITHUB_ACTIONS_SETUP.md       # This guide
```

## 🎯 Next Steps

1. ✅ Set up GitHub secrets
2. ✅ Update workflow configuration
3. ✅ Push code to trigger deployment
4. ✅ Monitor deployment in GitHub Actions
5. ✅ Test your deployed application
6. ✅ Set up monitoring and alerts

---

**🚀 This approach is simpler than Azure Key Vault and perfect for CI/CD deployments!**