# scripts/find_main_file.py

import os

def find_main_file(repo_path):
    main_candidates = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if 'if __name__' in content:
                        main_candidates.append(os.path.join(root, file))
    
    if main_candidates:
        print(f"Potential main files found: {main_candidates}")
    else:
        print("No typical main file found.")
    
    return main_candidates

if __name__ == "__main__":
    repo_path = input("Enter the path to the repository: ")
    find_main_file(repo_path)
