# ReadDepthOptimizer
- This script use a random sampling method to determine the minimum read threshold when given input values for %CV (coefficient of variation) and an expected cutoff.
- In-silico datasets were generated with specific parameters.
- Sub-sample read depths were tested, ranging from 1,000 to 100,000 in increments of 1,000.
- Each sub-sample was evaluated to see if it exceeded the target cutoff.
- This process was repeated 1,000 times to estimate the probability of correct classification for each sub-sample depth.
- The minimum read threshold was defined as the lowest sub-sample read depth achieving a 95% probability of accurate detection.
- To account for sampling biases, the entire process was repeated 100 times, and the average minimum read threshold was recorded.
