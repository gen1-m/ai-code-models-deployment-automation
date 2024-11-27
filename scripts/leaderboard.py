# leaderboard.py

import pandas as pd
import os
import logging

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def update_leaderboard(repo_url, metrics, leaderboard_path='leaderboard.csv'):
    """Add model metrics to the leaderboard and save it."""
    new_entry = {'repo_url': repo_url, **metrics}

    if not os.path.exists(leaderboard_path):
        df = pd.DataFrame(columns=['repo_url', 'accuracy', 'precision', 'recall', 'f1_score'])
    else:
        df = pd.read_csv(leaderboard_path)

    df = df.append(new_entry, ignore_index=True)
    df.to_csv(leaderboard_path, index=False)
    logging.info(f"Updated leaderboard: {leaderboard_path}")

def display_leaderboard(leaderboard_path='leaderboard.csv'):
    """Display the leaderboard sorted by accuracy."""
    if os.path.exists(leaderboard_path):
        df = pd.read_csv(leaderboard_path)
        logging.info(df.sort_values(by='accuracy', ascending=False))
    else:
        logging.info("Leaderboard file not found.")
