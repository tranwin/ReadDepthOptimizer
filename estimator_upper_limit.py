import csv
import numpy as np

# Set parameters
n = 1000000  # Sample size
tr = 0.0331814 # Positive rate
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
            result = sum(1 for count in topr if count / dep < 0.0346)

            # Add result to the current trial column
            row[f'trial_{trial+1}'] = result

            # Record dep value if the result is greater than 950
            if result > 950:
                last_result_dep_values[f'trial_{trial+1}'] = dep

        # Write the row to the CSV file
        writer.writerow(row)

    # Prepare the final row with the recorded dep values where the result was > 950
#     final_row = {'dep': 'dep_value > 950'}
#     final_row.update(last_result_dep_values)

#     # Write the final row to the CSV file
#     writer.writerow(final_row)

print(f"Results have been saved to {csv_file_name}")
