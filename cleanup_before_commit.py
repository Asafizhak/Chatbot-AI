#!/usr/bin/env python3
"""
Script to clean up repository before committing to Git
This removes files with hardcoded secrets and shows what's safe to commit
"""

import os
import glob

def check_file_for_secrets(filepath):
    """Check if a file contains potential secrets"""
    secret_indicators = [
        'AKIA',  # AWS access key prefix
        'client_secret',
        'password',
        'secret_key',
    ]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for indicator in secret_indicators:
                if indicator.lower() in content:
                    return True
    except:
        pass
    return False

def main():
    print("🧹 Repository Cleanup Before Git Commit")
    print("=" * 50)
    
    # Files that should be removed (contain secrets)
    files_to_remove = [
        'setup_keyvault_secrets.py',
        'run_setup.py', 
        'setup_env.bat',
        'config_secure.py',
        '.env'
    ]
    
    print("\n🗑️  Removing files with secrets:")
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   ✅ Removed: {file}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file}: {e}")
        else:
            print(f"   ℹ️  Not found: {file}")
    
    # Check remaining Python files for secrets
    print("\n🔍 Checking remaining files for secrets:")
    python_files = glob.glob('*.py')
    safe_files = []
    risky_files = []
    
    for file in python_files:
        if file == __file__.split('/')[-1]:  # Skip this script
            continue
            
        if check_file_for_secrets(file):
            risky_files.append(file)
            print(f"   ⚠️  {file} - May contain secrets!")
        else:
            safe_files.append(file)
            print(f"   ✅ {file} - Looks clean")
    
    # Show files safe to commit
    print("\n📁 Files safe to commit:")
    safe_to_commit = [
        'Asafiz-Ai-Simple.py',
        'config.py',
        'azure_keyvault_config.py',
        'requirements-simple.txt',
        'Dockerfile',
        '.gitignore',
        '.github/workflows/deploy-to-aks.yml',
        'k8s/deployment.yaml',
        'k8s/service.yaml',
        'GITHUB_ACTIONS_SETUP.md',
        'AZURE_KEYVAULT_SETUP.md',
        'FILES_TO_COMMIT.md'
    ]
    
    for file in safe_to_commit:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ Missing: {file}")
    
    # Summary
    print("\n📊 Summary:")
    print(f"   Safe files: {len(safe_files)}")
    print(f"   Risky files: {len(risky_files)}")
    
    if risky_files:
        print(f"\n⚠️  WARNING: These files may contain secrets:")
        for file in risky_files:
            print(f"   - {file}")
        print("\n   Review these files before committing!")
    else:
        print("\n✅ All Python files look clean!")
    
    print("\n🚀 Next steps:")
    print("1. Review any risky files listed above")
    print("2. Set your GitHub repository secrets")
    print("3. Run: git add .")
    print("4. Run: git commit -m 'Deploy ChatBot AI with GitHub Actions'")
    print("5. Run: git push origin main")
    
    print("\n🔐 Remember: Your AWS credentials should only be in GitHub Secrets!")

if __name__ == "__main__":
    main()