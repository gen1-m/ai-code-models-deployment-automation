# repo_manager.py

import os
import git
import subprocess

def clone_repository(repo_url, repo_path='repositories'):
    """Clone a GitHub repository into a specified path."""
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    local_path = os.path.join(repo_path, repo_name)
    if not os.path.exists(local_path):
        print(f"Cloning repository: {repo_url}")
        git.Repo.clone_from(repo_url, local_path)
    else:
        print(f"Repository already cloned: {repo_url}")
    return local_path

def install_dependencies(repo_path):
    """Install dependencies for the repository."""
    requirements_path = os.path.join(repo_path, 'requirements.txt')
    if os.path.exists(requirements_path):
        print(f"Installing dependencies from {requirements_path}")
        subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
    else:
        # Try to generate requirements.txt using pipreqs
        print(f"Generating requirements.txt using pipreqs for {repo_path}")
        subprocess.run(['pipreqs', repo_path], check=True)
        # Retry installation after generating
        if os.path.exists(requirements_path):
            subprocess.run(['pip', 'install', '-r', requirements_path], check=True)

