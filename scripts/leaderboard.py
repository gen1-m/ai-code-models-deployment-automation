# scripts/leaderboard.py

import csv

def update_leaderboard(model_name, accuracy, precision, recall, f1, leaderboard_file="data/evaluations.csv"):
    with open(leaderboard_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([model_name, accuracy, precision, recall, f1])
    print(f"Updated leaderboard with {model_name}.")

if __name__ == "__main__":
    model_name = input("Enter the model name: ")
    accuracy = float(input("Enter accuracy: "))
    precision = float(input("Enter precision: "))
    recall = float(input("Enter recall: "))
    f1 = float(input("Enter F1 score: "))
    update_leaderboard(model_name, accuracy, precision, recall, f1)
