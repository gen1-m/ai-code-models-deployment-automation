# scripts/generate_requirements.py

import os
import subprocess

def generate_requirements(repo_path):
    print(f"Generating requirements for {repo_path}...")
    
    try:
        # Using pipreqs to generate requirements.txt
        subprocess.run(["pipreqs", repo_path, "--force"], check=True)
        print("Generated requirements.txt using pipreqs.")
        
        # Use pip-chill to ensure completeness
        with open(os.path.join(repo_path, 'requirements.txt'), 'a') as f:
            subprocess.run(["pip-chill"], stdout=f, check=True)
        print("Appended missing packages using pip-chill.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating requirements: {e}")

if __name__ == "__main__":
    repo_path = input("Enter the path to the repository: ")
    generate_requirements(repo_path)
