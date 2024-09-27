# scripts/parse_readme.py

import os
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Set up Hugging Face API key as an environment variable (alternatively, you could authenticate via huggingface_hub)
huggingface_token = os.getenv("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")

# Load a model from Hugging Face's transformers library
tokenizer = AutoTokenizer.from_pretrained("t5-small")  # You can choose a different model like "gpt-2"
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

# Create a summarization pipeline
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def parse_readme_for_instructions(repo_path):
    readme_path = os.path.join(repo_path, 'README.md')
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            readme_content = f.read()
            
        # Use the summarization pipeline to extract instructions
        summary = summarizer(readme_content, max_length=150, min_length=30, do_sample=False)
        instructions = summary[0]['summary_text']
        print(f"Instructions extracted from README:\n{instructions}")
    else:
        print("No README.md found in the repository.")

if __name__ == "__main__":
    repo_path = input("Enter the path to the repository: ")
    parse_readme_for_instructions(repo_path)
