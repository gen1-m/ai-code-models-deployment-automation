# repo_manager.py

from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel
from utils import clean_requirements_output
import os
import git
import subprocess


# Load the tokenizer and model manually
tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
model = GPT2LMHeadModel.from_pretrained("distilgpt2")

# Ensure padding token is defined (since distilgpt2 doesn't have a pad token)
tokenizer.pad_token = tokenizer.eos_token

# Set up the pipeline using the explicitly configured tokenizer and model
dependency_resolver = pipeline(
    'text-generation',
    model=model,
    tokenizer=tokenizer
)

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

def setup_dependencies(repo_path):
    """Try to install dependencies and handle conflicts using Hugging Face LLM."""
    requirements_path = os.path.join(repo_path, 'requirements.txt')

    if os.path.exists(requirements_path):
        try:
            subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
        except subprocess.CalledProcessError:
            print(f"Conflict detected while installing from {requirements_path}. Attempting to resolve with LLM agent.")
            resolve_dependency_conflicts(requirements_path)
    else:
        # Generate requirements.txt with pipreqs and verify with pip-chill
        print("Generating requirements.txt using pipreqs")
        subprocess.run(['pipreqs', repo_path], check=True)
        pip_chill_output = subprocess.run(['pip-chill'], capture_output=True, text=True)
        
        with open(requirements_path, 'w') as file:
            file.write(pip_chill_output.stdout)

        # Attempt to install again
        try:
            subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
        except subprocess.CalledProcessError:
            print("Dependencies installation failed after generating requirements.txt. Trying to resolve with LLM.")
            resolve_dependency_conflicts(requirements_path)

def resolve_dependency_conflicts(requirements_path):
    """Use Hugging Face LLM to resolve dependency conflicts in requirements.txt."""
    with open(requirements_path, 'r') as file:
        requirements = file.read()

    # Prompt to fix requirements
    prompt = f"""
    The following requirements.txt has conflicting dependencies:
    {requirements}

    Correct these conflicts and provide only the fixed requirements list without any explanations or additional text.
    Each package should be on a separate line in a valid requirements.txt format:
    """

    # Generate response using adjusted model settings
    response = dependency_resolver(
        prompt,
        max_new_tokens=200,  # Use max_new_tokens instead of max_length for output length
        num_return_sequences=1,
        truncation=True,  # Explicitly enable truncation
        pad_token_id=tokenizer.eos_token_id  # Explicitly set pad_token_id to eos_token_id
    )[0]['generated_text']

    # Clean and validate the generated requirements
    corrected_requirements = clean_requirements_output(response)

    with open(requirements_path, 'w') as file:
        file.write(corrected_requirements)

    # Retry installation
    try:
        subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install dependencies after LLM conflict resolution. Manual intervention may be required.")
