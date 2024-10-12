# main.py

from repo_manager import clone_repository, install_dependencies
from script_identifier import find_main_script
from model_runner import run_model
from evaluator import evaluate_model
from leaderboard import update_leaderboard, display_leaderboard

def process_repository(repo_url):
    """Complete process for cloning, running, and evaluating a repository."""
    repo_path = clone_repository(repo_url)
    install_dependencies(repo_path)
    main_script = find_main_script(repo_path)
    model_output = run_model(repo_path, main_script)
    if model_output:
        metrics = evaluate_model(model_output)
        update_leaderboard(repo_url, metrics)

if __name__ == "__main__":
    repos = [
        "https://github.com/user/repo1",
        "https://github.com/user/repo2"
    ]

    for repo_url in repos:
        process_repository(repo_url)

    # Display the final leaderboard
    display_leaderboard()
