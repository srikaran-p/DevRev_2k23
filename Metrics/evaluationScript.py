import ast
import json
from evaluationMetrics import Metrics

def convert_strings_in_json(json_string):
    # Load the JSON string
    json_data = json.loads(json_string)

    # Helper function to recursively convert strings containing lists
    def convert_value(value):
        if isinstance(value, str):
            try:
                # Attempt to evaluate the string as a literal using ast.literal_eval
                return ast.literal_eval(value)
            except (SyntaxError, ValueError):
                # If evaluation fails, return the original string
                return value
        elif isinstance(value, list):
            # Recursively convert strings within the list
            return [convert_value(item) for item in value]
        elif isinstance(value, dict):
            # Recursively convert strings within the dictionary values
            return {key: convert_value(val) for key, val in value.items()}
        else:
            return value

    # Recursively convert strings within the entire JSON data
    converted_data = convert_value(json_data)

    return converted_data

exp_file = open('test_data.json')

exp_data = json.load(exp_file)
# exp_data = convert_strings_in_json(exp_data)

exp_ans = []
exp_que = []

for exp in exp_data:
    exp_ans.append(exp['answer'])
    exp_que.append(exp['question'])

pred_file = open('gpt-4.json')

print(exp_ans)

pred_data = json.load(pred_file)
# pred_data = convert_strings_in_json(pred_data)

pred_ans = []
pred_que = []

for pref in pred_data:
    pred_ans.append(pref['answer'])
    pred_que.append(pref['question'])

metrics = Metrics()

em_score = 0
f1_score = 0

for i in range(len(pred_data)):
    if metrics.exactMatch(pred_ans[i], exp_ans[i]) == True:
        em_score += 1
    else:
        # print(i)
        pass

    try:
        f1_value = metrics.f1_score_overall(pred_ans[i], exp_ans[i])
        f1_score += f1_value
    except:
        print(i, " index does not work")
        pass

index = 0
print(exp_que[index])
print()
print(pred_que[index])
print()
print(exp_ans[index])
print()
print(pred_ans[index])
print()
print(metrics.exactMatch(pred_ans[index], exp_ans[index]))
print()
try:
    print(metrics.f1_score_overall(pred_ans[index], exp_ans[index]))
except:
    print("Division by zero")
print()

print("\nOverall EM Score: ", em_score/len(pred_data))
print("\nOverall F1 Score: ", f1_score/len(pred_data))
