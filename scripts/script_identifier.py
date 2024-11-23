# script_identifier.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("PROFESSORS_API_KEY"))

def find_python_files(repo_path):
    """Recursively find all Python files in the repository."""
    python_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def find_main_script(repo_path):
    """Identify the main script to run the model."""
    # Check for conventional main scripts in the root directory
    for script_name in ['main.py', 'train.py', 'run.py']:
        potential_path = os.path.join(repo_path, script_name)
        if os.path.exists(potential_path):
            print(f"Found main script: {script_name}")
            return script_name

    # No conventional main script found, use LLM to identify a potential entry point
    print("No conventional main script found. Attempting to identify using LLM.")
    python_files = find_python_files(repo_path)

    for script_path in python_files:
        with open(script_path, 'r') as file:
            content = file.read()

            # Build a detailed prompt for analysis
            relative_path = os.path.relpath(script_path, repo_path)
            prompt = f"""
            You are analyzing the structure of a machine learning repository.
            
            Below is the content of a Python script located at `{relative_path}`:
            ---
            {content}
            ---
            Determine if this script is the main entry point for running a machine learning model. 
            This means the script should contain functionalities like training loops, evaluation routines, or command-line arguments.
            
            Respond with 'yes' or 'no' and provide a brief explanation:
            """

            try:
                # Call OpenAI's ChatGPT API
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="gpt-4",
                    temperature=0,
                    max_tokens=300
                )

                # Extract and process the response
                decision = response.choices[0].message.content.strip().lower()

                if 'yes' in decision:
                    print(f"Identified entry point in: {relative_path}")
                    return relative_path

            except Exception as e:
                print(f"Error while analyzing {relative_path} with OpenAI API: {e}")

    print("Unable to identify an entry point. Proceeding to README analysis.")
    return None
