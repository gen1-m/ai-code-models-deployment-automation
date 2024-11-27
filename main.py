# main.py
Import logging
from scripts.repo_manager import clone_repository, setup_dependencies
from scripts.script_identifier import find_main_script
from scripts.model_runner import run_model
from scripts.evaluator import evaluate_model
from scripts.leaderboard import update_leaderboard, display_leaderboard
from scripts.readme_parser import generate_main_script_from_readme

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",        # Use append mode for the log file
)

def process_repository(repo_url):
    """Complete process for cloning, running, and evaluating a repository."""
    try: 
        logging.info(f"Starting processing for repository: {repo_url}")


        repo_path = clone_repository(repo_url)
        logging.info(f"Cloned repository to: {repo_path}")

        setup_dependencies(repo_path)
        logging.info(f"Dependencies set up for repository: {repo_path}")

        main_script = find_main_script(repo_path)

        if not main_script:
        # Generate main script from README if none found
        # logging.warning("Main script not found. Attempting to generate from README.")
            main_script = generate_main_script_from_readme(repo_path)

        model_output = run_model(repo_path, main_script)
        if model_output:
            metrics = evaluate_model(model_output)
            update_leaderboard(repo_url, metrics)

    except Exception as e:
         logging.error(f"Error processing repository {repo_url}: {e}", exc_info=True)

if __name__ == "__main__":
    repos = [
        "https://github.com/anubhavparas/image-classification-using-cnn.git",
    ]

    for repo_url in repos:
        process_repository(repo_url)

    # Display the final leaderboard
    display_leaderboard()


