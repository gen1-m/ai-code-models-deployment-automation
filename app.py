# app.py

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from scripts.clone_repo import clone_repo
from scripts.generate_requirements import generate_requirements
from scripts.find_main_file import find_main_file
from scripts.parse_readme import parse_readme_for_instructions
from scripts.evaluate_model import run_model_and_evaluate
from scripts.leaderboard import update_leaderboard

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_repository(repo_url):
    try:
        logging.info(f"Processing repository: {repo_url}")
        repo_path = clone_repo(repo_url)
        
        generate_requirements(repo_path)
        
        main_files = find_main_file(repo_path)
        
        if not main_files:
            parse_readme_for_instructions(repo_path)
        else:
            accuracy, precision, recall, f1 = run_model_and_evaluate(main_files[0])
            update_leaderboard(repo_path.split('/')[-1], accuracy, precision, recall, f1)
        
        logging.info(f"Successfully processed repository: {repo_url}")
    
    except Exception as e:
        logging.error(f"Error processing repository {repo_url}: {e}")

def main():
    # Read repository URLs from a file
    with open("repositories.txt", "r") as file:
        repo_urls = file.readlines()

    # Remove any extra whitespace/newlines and filter out empty lines
    repo_urls = [url.strip() for url in repo_urls if url.strip()]

    # Process repositories in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        futures = {executor.submit(process_repository, url): url for url in repo_urls}

        for future in as_completed(futures):
            repo_url = futures[future]
            try:
                future.result()  # If an exception was raised, it will be re-raised here
            except Exception as e:
                logging.error(f"Exception occurred for {repo_url}: {e}")

if __name__ == "__main__":
    main()
