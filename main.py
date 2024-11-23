# main.py

from scripts.repo_manager import clone_repository, setup_dependencies
from scripts.script_identifier import find_main_script
from scripts.model_runner import run_model
from scripts.evaluator import evaluate_model
from scripts.leaderboard import update_leaderboard, display_leaderboard
from scripts.readme_parser import generate_main_script_from_readme

def process_repository(repo_url):
    """Complete process for cloning, running, and evaluating a repository."""
    repo_path = clone_repository(repo_url)
    setup_dependencies(repo_path)
    main_script = find_main_script(repo_path)

    if not main_script:
        # Generate main script from README if none found
        main_script = generate_main_script_from_readme(repo_path)

    model_output = run_model(repo_path, main_script)
    if model_output:
        metrics = evaluate_model(model_output)
        update_leaderboard(repo_url, metrics)

if __name__ == "__main__":
    repos = [
        "https://github.com/anubhavparas/image-classification-using-cnn.git",
    ]

    for repo_url in repos:
        process_repository(repo_url)

    # Display the final leaderboard
    display_leaderboard()

