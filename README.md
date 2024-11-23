# AI Code Models Deployment Automation

This repository contains the code for the AI Code Models Deployment Automation project. 
The project aims to automate the process of evaluating and machine learning models for code repositories, and comparing their performance against each other. 
The results are then used to generate a leaderboard for the repository.

## Collaborators

- [Eugen Mamaj](https://github.com/gen1-m)
- [Mary Grigoryan](https://github.com/Mery101010)

## Project Structure

The project is structured as follows:

```
├── .gitignore
├── README.md
├── scripts
│   ├── evaluator.py
│   ├── leaderboard.py
│   ├── model_runner.py
│   ├── readme_parser.py
│   ├── repo_manager.py
│   ├── script_identifier.py
├── utils.py
└── requirements.txt
├── main.py
```
### Prerequisites

Before running the project, ensure you have the following installed:

- [Python >= 3.10](https://www.python.org/downloads/)
- [Git](https://github.com/git-guides/install-git)

Also you need to have an OpenAI API key. You can get one [here](https://platform.openai.com/account/api-keys).

You should set the API key by creating a `.env` file in the root directory of the project and adding the following line:

```
OPENAI_API_KEY=YOUR_API_KEY
```

After that, the project structure should look like this:

```
├── .env
├── .gitignore
├── README.md
├── scripts
│   ├── evaluator.py
│   ├── leaderboard.py
│   ├── model_runner.py
│   ├── readme_parser.py
│   ├── repo_manager.py
│   ├── script_identifier.py
├── utils.py
└── requirements.txt
├── main.py
``` 

## Usage

To run the project, follow these steps:

1. Clone the repository using https or ssh:

```bash
git clone https://github.com/eugenm/ai-code-models-deployment-automation.git
```

2. Set up the environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3.  Run the main script:

```bash
python main.py
```

This will clone the repositories, install their dependencies, and run the evaluation process. You will see then that you have a newly genrated 'leaderboard.csv' file in the root directory of the project.
