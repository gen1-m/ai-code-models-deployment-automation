# script_identifier.py

import os
from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel

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

def find_main_script(repo_path):
    """Identify the main script to run the model."""
    for script_name in ['main.py', 'train.py', 'run.py']:
        potential_path = os.path.join(repo_path, script_name)
        if os.path.exists(potential_path):
            print(f"Found main script: {script_name}")
            return script_name

    # No conventional main script found, use LLM to identify a potential entry point
    print("No conventional main script found. Attempting to identify using LLM.")
    repo_files = [f for f in os.listdir(repo_path) if f.endswith('.py')]
    for script in repo_files:
        with open(os.path.join(repo_path, script), 'r') as file:
            content = file.read()
            prompt = f"""
            Analyze the following Python script and determine if it can be the entry point for a machine learning model:
            {content}
            Does this script contain the main entry point (e.g., training loop, command-line arguments)? Respond with 'yes' or 'no' and why.
            """
            response = dependency_resolver(
                prompt,
                max_new_tokens=150,  # Use max_new_tokens for the output
                num_return_sequences=1,
                truncation=True,  # Enable truncation
                pad_token_id=tokenizer.eos_token_id  # Explicitly set pad_token_id to eos_token_id
            )[0]['generated_text']

            if 'yes' in response.lower():
                print(f"Identified entry point in: {script}")
                return script

    print("Unable to identify an entry point. Proceeding to README analysis.")
    return None
