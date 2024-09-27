# scripts/evaluate_model.py

import os
import subprocess
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def run_model_and_evaluate(main_file):
    print(f"Running model from {main_file}...")
    subprocess.run(["python", main_file])
    # Assume that the model outputs predictions and true labels to a file
    y_pred = [...]  # Load predictions from file
    y_true = [...]  # Load true labels from file
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    print(f"Model Evaluation - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1: {f1}")
    
    return accuracy, precision, recall, f1

if __name__ == "__main__":
    main_file = input("Enter the path to the main file: ")
    run_model_and_evaluate(main_file)
