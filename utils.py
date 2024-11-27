import re
import logging

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def clean_requirements_output(raw_output):
    """Ensure the output is formatted as valid requirements.txt entries."""
    valid_lines = []
    pattern = re.compile(r'^[a-zA-Z0-9._-]+(==[0-9]+(\.[0-9]+)*)?$')
    for line in raw_output.splitlines():
        line = line.strip()
        # Remove any unexpected text, ensuring valid format for requirements
        if pattern.match(line):
            valid_lines.append(line)
        else:
            logging.warning(f"Invalid line detected: {line}")
            
    return "\n".join(valid_lines)
