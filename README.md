# ReadDepthOptimizer

- This script uses a random sampling method to determine the minimum read threshold based on input values for %CV (coefficient of variation) and an expected cutoff.
- In-silico datasets were generated with specific parameters.
- Sub-sample read depths were tested, ranging from 1,000 to 100,000 in increments of 1,000.
- Each sub-sample was evaluated to see if it exceeded the target cutoff.
- This process was repeated 1,000 times to estimate the probability of correct classification for each sub-sample depth.
- The minimum read threshold was defined as the lowest sub-sample read depth achieving a 95% probability of accurate detection.
- To account for sampling biases, the entire process was repeated 100 times, and the average minimum read threshold was recorded.

## To Run:

```bash
python estimate_upper_limit.py --n 500000 --threshold 0.05 --cv 10
```
Where
- n: Sample size or number of reads in your typical sample
- threshold: Your cutoff to determine a sample is positive or not
- cv: variation calculated from prior studies

