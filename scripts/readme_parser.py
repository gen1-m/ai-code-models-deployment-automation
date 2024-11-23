# readme_parser.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("PROFESSORS_API_KEY")  # Default is environment variable OPENAI_API_KEY
)

def generate_main_script_from_readme(repo_path):
    """
    Generate a main.py script by parsing the README.md using OpenAI's ChatGPT API.

    Args:
        repo_path (str): Path to the repository containing the README.md file.

    Returns:
        str or None: Path to the generated script ('main.py') or None if the README.md is not found.
    """
    readme_path = os.path.join(repo_path, 'README.md')
    if not os.path.exists(readme_path):
        print("No README.md found to generate the main script.")
        return None

    with open(readme_path, 'r') as file:
        readme_content = file.read()

    # Define the detailed prompt
    prompt = f"""
    You are an expert Python programmer. Based on the following README.md content, generate a Python script named 'main.py' that automates the steps required to run the project. Ensure the script is runnable and includes comments explaining each step.

    If the README.md describes installation steps, dependencies, or commands to run, translate those into Python code.

    README.md content:
    ---
    {readme_content}
    ---

    Output the complete 'main.py' script:
    """

    try:
        # Call OpenAI's ChatGPT API using the client
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",  # Use your preferred model here, e.g., "gpt-4"
            temperature=0.7,
            max_tokens=1000
        )
        
        # Correctly access the generated content
        generated_script = response.choices[0].message.content.strip()

        # Save the generated script as 'main.py' in the repository
        main_script_path = os.path.join(repo_path, 'main.py')
        with open(main_script_path, 'w') as file:
            file.write(generated_script)

        print(f"Generated main.py at {main_script_path}")
        return 'main.py'

    except Exception as e:
        print(f"Error while generating the script with OpenAI API: {e}")
        return None

