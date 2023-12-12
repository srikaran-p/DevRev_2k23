# Evaluation Metrics

## Metrics Calculation

The evaluationMetrics.py script contains a class Metrics that implements various metrics for evaluating the performance of models. The metrics include:

- exactMatch: Determines if two JSON objects are exactly the same.
- f1_score_overall: Calculates the overall F1 score for predicted and required JSON lists.
- hallucination_rate: Computes the overall hallucination rate for tools and arguments.

Additionally, the class includes several helper functions such as precision, recall, and set_difference_operator for detailed metric calculations.

python
import json

class Metrics:
    # ... (class implementation)

# Example Usage:
metrics = Metrics()
metrics.exactMatch(a, b)
metrics.hallucination_rate(given_json, predicted_json)
metrics.f1_score_overall(predictedJson, requiredJson)