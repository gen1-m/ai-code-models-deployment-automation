# readme_parser.py

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

def generate_main_script_from_readme(repo_path):
    """Generate a main.py script by parsing the README.md."""
    readme_path = os.path.join(repo_path, 'README.md')
    if not os.path.exists(readme_path):
        print("No README.md found to generate main script.")
        return None

    with open(readme_path, 'r') as file:
        readme_content = file.read()

    # Use Hugging Face LLM to generate a script based on README instructions
    prompt = f"""
    The following is a README.md content that describes how to run a machine learning model:
    {readme_content}

    Based on this information, create a Python script (main.py) that follows the steps to run the model:
    """
    response = dependency_resolver(
        prompt,
        max_new_tokens=800,  # Use max_new_tokens instead of max_length
        num_return_sequences=1,
        truncation=True,  # Enable truncation
        pad_token_id=tokenizer.eos_token_id  # Explicitly set pad_token_id
    )[0]['generated_text']

    # Save the generated script
    main_script_path = os.path.join(repo_path, 'main.py')
    with open(main_script_path, 'w') as file:
        file.write(response.strip())

    print(f"Generated main.py at {main_script_path}")
    return 'main.py'

