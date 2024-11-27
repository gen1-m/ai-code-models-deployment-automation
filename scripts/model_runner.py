# model_runner.py

import subprocess
import os
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_model(repo_path, main_script):
    """Run the identified main script and capture output."""
    if main_script:
        script_path = os.path.join(repo_path, main_script)
        try:
            logging.info(f"Running model script: {script_path}")
            result = subprocess.run(
                ['python', script_path], 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.info(f"Error occurred while running the script: {e}")
            return None
    return None
