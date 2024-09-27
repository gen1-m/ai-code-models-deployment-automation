import os
import git

def clone_repo(repo_url, clone_dir="./repos"):
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(clone_dir, repo_name)
    
    if not os.path.exists(repo_path):
        git.Repo.clone_from(repo_url, repo_path)
        print(f"Cloned {repo_url} to {repo_path}")
    else:
        print(f"Repository {repo_name} already exists at {repo_path}")
    
    return repo_path

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    clone_repo(repo_url)
