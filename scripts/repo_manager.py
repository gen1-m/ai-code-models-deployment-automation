import os
import git
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import re
from utils import clean_requirements_output

# Ensure environment variables are loaded
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("PROFESSORS_API_KEY"))

# Known mapping of import names to pip install names
import_to_pip_mapping = {
    "cv2": "opencv-python",  # opencv package is imported as cv2 but installed as opencv-python
    "tensorflow": "tensorflow",  # Same name for both install and import
    "torch": "torch",  # Same name for both install and import
    "pandas": "pandas",  # Same name for both install and import
    "sklearn": "scikit-learn",  # scikit-learn is imported as sklearn
    "flask": "flask",  # Same name for both install and import
    "requests": "requests",  # Same name for both install and import
    "beautifulsoup4": "beautifulsoup4",  # Same name for both install and import
    # Add more common mappings as needed
}

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

def extract_imports_from_files(repo_path):
    """
    Extract all imported packages from Python files in the repository.
    Excludes local module imports by checking the existence of the module in the repo.
    """
    imported_packages = set()
    local_modules = set()

    # Collect all local module names (files and directories in the repo)
    for root, dirs, files in os.walk(repo_path):
        for name in files:
            if name.endswith('.py'):
                local_modules.add(os.path.splitext(name)[0])  # Add module names (without .py)
        for name in dirs:
            local_modules.add(name)  # Add directory names (potential module folders)

    # Parse imports from Python files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors="ignore") as f:
                    for line in f:
                        match = re.match(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', line)
                        if match:
                            module_name = match.group(1)
                            # If it's not a local module, consider it a pip package
                            if module_name not in local_modules:
                                imported_packages.add(module_name)

    return imported_packages

def compare_requirements_with_imports(requirements_path, imported_packages):
    """Compare imports with requirements.txt and identify missing packages."""
    existing_packages = set()
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as file:
            for line in file:
                package = line.split('==')[0].strip()  # Extract package name without version
                existing_packages.add(package)

    missing_packages = imported_packages - existing_packages
    return missing_packages

def map_import_to_pip_package(import_name):
    """Map import names to pip install package names using the predefined mapping."""
    return import_to_pip_mapping.get(import_name, import_name)

def install_missing_packages(missing_packages):
    """Install missing packages directly using pip."""
    for package in missing_packages:
        # Check if the import name matches a known mapping for installation
        install_package = map_import_to_pip_package(package)
        
        try:
            print(f"Installing missing package: {install_package}")
            subprocess.run(['pip', 'install', install_package], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to install package: {install_package}. Please check manually.")

def setup_dependencies(repo_path):
    """Install dependencies and ensure all required packages are included."""
    requirements_path = os.path.join(repo_path, 'requirements.txt')

    # Extract imported packages from all Python files in the repository
    print("Extracting imported packages...")
    imported_packages = extract_imports_from_files(repo_path)

    # Compare and identify missing packages
    missing_packages = compare_requirements_with_imports(requirements_path, imported_packages)

    # Install missing packages directly with pip
    if missing_packages:
        print("Missing packages detected. Installing missing packages...")
        install_missing_packages(missing_packages)

    # Now that all dependencies are installed, generate the updated requirements.txt
    try:
        print("Generating updated requirements.txt using pip freeze...")
        subprocess.run(['pip', 'freeze'], stdout=open(requirements_path, 'w'), check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to generate updated {requirements_path}. Please check manually.")

def resolve_dependency_conflicts(requirements_path):
    """Use OpenAI's LLM to resolve dependency conflicts in requirements.txt."""
    with open(requirements_path, 'r') as file:
        requirements = file.read()

    # Prompt to fix requirements
    prompt = f"""
    The following requirements.txt has missing or conflicting dependencies:
    {requirements}

    Correct these issues and provide a fixed requirements list without any explanations or additional text.
    Each package should be on a separate line in valid requirements.txt format:
    """

    try:
        # Call OpenAI's ChatGPT API using the client
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",
            temperature=0,
            max_tokens=200
        )

        # Extract the generated requirements
        corrected_requirements = response.choices[0].message.content.strip()

        # Clean and validate the generated requirements
        corrected_requirements = clean_requirements_output(corrected_requirements)

        with open(requirements_path, 'w') as file:
            file.write(corrected_requirements)

        # Retry installation
        try:
            subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
        except subprocess.CalledProcessError:
            print("Failed to install dependencies after LLM conflict resolution. Manual intervention may be required.")

    except Exception as e:
        print(f"Error while resolving dependency conflicts with OpenAI API: {e}")
