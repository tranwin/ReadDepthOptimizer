import csv
import numpy as np
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Run simulations and save results to a CSV file.')
parser.add_argument('--n', type=int, default=1000000, help='Sample size')
parser.add_argument('--threshold', type=float, required=True, help='Threshold for proportion of 1s')
parser.add_argument('--cv', type=float, required=True, help='Coefficient of Variation as a percentage')
args = parser.parse_args()

# Set parameters from arguments
n = args.n
threshold = args.threshold
cv = args.cv / 100  # Convert %CV to a decimal

# Calculate tr based on CV
tr = threshold * (1 + cv)
ntr = int(n * tr)  # Number of trials (converted to integer)
rep = 1000  # Number of repetitions
num_trials = 100  # Number of datasets to generate

# Values of dep
dep_values = list(range(1000, 100001, 1000))

# Convert tr to a string without decimal point for filename
tr_str = str(tr).replace(".", "")
n_str = str(n)

# Open CSV file for writing
csv_file_name = f'results_samplesize_{n}_{tr_str}_100K_100trials.csv'
with open(csv_file_name, 'w', newline='') as csvfile:
    # Field names will include the 'dep' column and 100 trial result columns
    fieldnames = ['dep'] + [f'trial_{i+1}' for i in range(num_trials)]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    last_result_dep_values = {f'trial_{i+1}': None for i in range(num_trials)}

    for dep in dep_values:
        row = {'dep': dep}

        for trial in range(num_trials):
            # Generate data vector
            dat = np.concatenate((np.ones(ntr), np.zeros(n - ntr)))

            topr = []  # Initialize empty list for storing results

            # Perform simulations
            for i in range(rep):
                ts1 = np.random.choice(dat, size=dep)  # Sample 'dep' elements randomly
                topr.append(np.sum(ts1))  # Count occurrences of 1 in the sample and append to topr

            # Count the number of occurrences where the proportion of 1s is greater than the threshold
            result = sum(1 for count in topr if count / dep < threshold)

            # Add result to the current trial column
            row[f'trial_{trial+1}'] = result

            # Record dep value if the result is greater than 950
            if result > 950:
                last_result_dep_values[f'trial_{trial+1}'] = dep

        # Write the row to the CSV file
        writer.writerow(row)

print(f"Results have been saved to {csv_file_name}")
