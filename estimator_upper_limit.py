"""
This script runs simulations and saves results into two CSV files based on threshold comparisons.

Author: Tran Nguyen

How to run:
    python script_name.py --n SAMPLE_SIZE --threshold THRESHOLD_VALUE --cv CV_VALUE

Parameters:
    --n            : (Optional) The sample size. Default is 1000000.
    --threshold    : The threshold value for the proportion of 1s (required).
    --cv           : The coefficient of variation as a percentage (required).

Example:
    python min_dep_finder.py --threshold 1.7 --cv 9.4

This will create two CSV files for "lower" and "upper" threshold simulations.
"""

import csv
import numpy as np
import argparse
import pandas as pd

# Function to simulate and write results to CSV
def run_simulation(n, ntr, dep_values, threshold, file_name, comparison_operator):
    """
    Run simulations and write results to a CSV file.
    
    Parameters:
    - n: total sample size
    - ntr: calculated trials for the given threshold
    - dep_values: list of dep values to iterate
    - threshold: threshold for the proportion of 1s
    - file_name: name of the output CSV file
    - comparison_operator: comparison operator (< or >) for threshold
    """
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['dep'] + [f'trial_{i+1}' for i in range(num_trials)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for dep in dep_values:
            row = {'dep': dep}
            for trial in range(num_trials):
                dat = np.concatenate((np.ones(ntr), np.zeros(n - ntr)))
                topr = [np.sum(np.random.choice(dat, size=dep)) for _ in range(rep)]

                # Apply threshold comparison (either < or > depending on the scenario)
                result = sum(1 for count in topr if (count / dep < threshold if comparison_operator == "<" else count / dep > threshold))
                row[f'trial_{trial+1}'] = result

            writer.writerow(row)
    print(f"Results have been saved to {file_name}")

# Function to find minimum dep values and calculate average
def find_minimum_deps(csv_file):
    """
    Read the CSV file and find the minimum dep values where trial results exceed 950.
    """
    df = pd.read_csv(csv_file)
    min_deps = []

    for col in df.columns[1:]:
        min_dep = None
        for _, row in df.iterrows():
            dep = row['dep']
            trial_value = row[col]

            if trial_value > 950:
                min_dep = dep
                break  # We only need the first dep value greater than 950
        
        if min_dep:
            min_deps.append(min_dep)

    # Calculate the average of the minimum dep values
    average_dep = sum(min_deps) / len(min_deps) if min_deps else None
    return min_deps, average_dep

# Function to export results to CSV
def export_results(min_deps, average_dep, file_name):
    """
    Export the minimum dep values and the average dep to a CSV file.
    """
    with open(file_name, 'w', newline='') as results_file:
        writer = csv.writer(results_file)
        writer.writerow(['Trial', 'Minimum dep value'])

        for i, value in enumerate(min_deps):
            writer.writerow([f'Trial {i+1}', value])

        if average_dep:
            writer.writerow([])
            writer.writerow(['Average of minimum dep values', average_dep])
        else:
            writer.writerow([])
            writer.writerow(['No valid dep values found'])

    print(f"Minimum dep values and average have been saved to {file_name}")

# Main execution
if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run simulations and save results to a CSV file.')
    parser.add_argument('--n', type=int, default=1000000, help='Sample size')
    parser.add_argument('--threshold', type=float, required=True, help='Threshold for proportion of 1s')
    parser.add_argument('--cv', type=float, required=True, help='Coefficient of Variation as a percentage')
    args = parser.parse_args()

    # Set parameters from arguments
    n = args.n
    threshold = args.threshold / 100
    cv = args.cv / 100  # Convert %CV to a decimal
    tr_lower = threshold - (threshold * cv)
    ntr_lower = int(n * tr_lower)
    tr_upper = threshold + (threshold * cv)
    ntr_upper = int(n * tr_upper)
    rep = 1000  # Number of repetitions
    num_trials = 100  # Number of datasets to generate
    dep_values = list(range(1000, 100001, 1000))

    # Lower threshold simulation
    csv_file_name_lower = f'results_samplesize_{n}_{str(tr_lower).replace(".", "")}_100K_100trials_lower.csv'
    run_simulation(n, ntr_lower, dep_values, threshold, csv_file_name_lower, "<")

    # Find and export minimum dep values for lower threshold
    min_deps_values, average_dep_value = find_minimum_deps(csv_file_name_lower)
    export_results(min_deps_values, average_dep_value, 'min_dep_results_lower.csv')

    # Upper threshold simulation
    csv_file_name_upper = f'results_samplesize_{n}_{str(tr_upper).replace(".", "")}_100K_100trials_upper.csv'
    run_simulation(n, ntr_upper, dep_values, threshold, csv_file_name_upper, ">")

    # Find and export minimum dep values for upper threshold
    min_deps_values, average_dep_value = find_minimum_deps(csv_file_name_upper)
    export_results(min_deps_values, average_dep_value, 'min_dep_results_upper.csv')
