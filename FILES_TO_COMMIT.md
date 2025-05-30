# 📁 Files to Commit vs Keep Local

## ✅ Safe to Commit to Git (No Secrets)

### Application Files
- `Asafiz-Ai-Simple.py` - Main application using environment variables
- `requirements-simple.txt` - Python dependencies
- `Dockerfile` - Container configuration

### Kubernetes & CI/CD
- `.github/workflows/deploy-to-aks.yml` - GitHub Actions workflow
- `k8s/deployment.yaml` - Kubernetes deployment
- `k8s/service.yaml` - Kubernetes service

### Configuration Templates (No Real Secrets)
- `config.py` - Now uses environment variables only
- `azure_keyvault_config.py` - Key Vault integration (if needed later)

### Documentation
- `GITHUB_ACTIONS_SETUP.md` - Setup guide
- `AZURE_KEYVAULT_SETUP.md` - Key Vault guide (reference)
- `FILES_TO_COMMIT.md` - This file

### Git Configuration
- `.gitignore` - Prevents committing secrets

## ❌ NEVER Commit to Git (Contains Secrets)

### Files with Hardcoded Credentials
- `setup_keyvault_secrets.py` - Contains real AWS credentials
- `run_setup.py` - Contains real AWS credentials
- `setup_env.bat` - May contain credentials
- `config_secure.py` - May contain credentials
- `.env` - Environment variables with secrets

### Local Development Files
- Any file ending with `_local.py`
- Any file ending with `_dev.py`
- Any `.env` files
- Any files with "secret", "key", "password" in the name

## 🧹 Cleanup Commands

Before committing to Git, run these commands to remove sensitive files:

```bash
# Remove files with secrets (they're already in .gitignore)
rm -f setup_keyvault_secrets.py
rm -f run_setup.py
rm -f setup_env.bat
rm -f config_secure.py
rm -f .env

# Check what will be committed
git status

# Make sure no secrets are in the files to be committed
git add --dry-run .
```

## 🔐 GitHub Secrets to Set

In your GitHub repository settings, add these secrets:

### Azure Credentials
- `ACR_USERNAME`
- `ACR_PASSWORD`
- `AZURE_CREDENTIALS`

### AWS Bedrock Credentials
- `AWS_ACCESS_KEY`
- `AWS_SECRET_KEY`
- `AWS_REGION`
- `MODEL_ID`
- `SYSTEM_PROMPT`

## 🚀 Safe Commit Process

1. **Review files**: Check each file for hardcoded secrets
2. **Test .gitignore**: Ensure sensitive files are ignored
3. **Commit clean code**: Only commit files from the "Safe to Commit" list
4. **Set GitHub secrets**: Add your credentials to GitHub repository secrets
5. **Deploy**: Push to trigger GitHub Actions deployment

---

**🔒 Remember: Once you commit to Git, assume the data is public forever!**