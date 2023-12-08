import ast
import json
from evaluationMetrics import Metrics

def string_to_list(string):
    new_list = []
    for item in string.split(','):
        item = item.strip().strip('\'').strip('\"').strip()
        new_list.append(item)
    return new_list

def string_to_dict(string):
    new_dict = {}
    for item in string.split(','):
        key = item.split(':')[0].strip().strip('\'').strip('\"').strip()
        value = item.split(':')[1].strip().strip('\'').strip('\"').strip()
        new_dict[key] = value
    return new_list


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


def calculate_metrics(toolset_ans , pred_ans , exp_ans):
    metrics = Metrics()

    em_score = 0
    f1_score = 0

    for i in range(len(pred_ans)):
        if metrics.exactMatch(pred_ans[i], exp_ans[i]) == True:
            em_score += 1

        try:
            f1_value = metrics.f1_score_overall(pred_ans[i], exp_ans[i])
            f1_score += f1_value
        except:
            print(i, " index does not work")
            pass

    overall_hallucination_rate = 0
    for i in range(len(pred_ans)):
        hallucination_rate_example = metrics.hallucination_rate(toolset_ans, pred_ans[i])
        overall_hallucination_rate += hallucination_rate_example

    print("Overall Hallucination Rate: ", overall_hallucination_rate/len(pred_data))
    print("\nOverall EM Score: ", em_score/len(pred_ans))
    print("\nOverall F1 Score: ", f1_score/len(pred_ans))


if __name__ == '__main__':
    exp_file = open('test_data.json')

    exp_data = json.load(exp_file)
    exp_ans = []
    exp_que = []

    for exp in exp_data:
        exp_ans.append(exp['answer'])
        exp_que.append(exp['question'])

    pred_file = open('gpt-4.json')

    pred_data = json.load(pred_file)

    pred_ans = []
    pred_que = []

    for pref in pred_data:
        pred_ans.append(pref['answer'])
        pred_que.append(pref['question'])

    # if a list or dictionary is being represented as a string, we manually parse
    for idx , ans in enumerate(pred_ans):
        for tool in ans:
            for arg in tool['arguments']:

                if isinstance(arg['argument_value'], str):

                    if arg['argument_value'] != '':
                        if arg['argument_value'].strip()[0] == '[' and arg['argument_value'].strip()[-1] == ']':
                            arg['argument_value'] = string_to_list(arg['argument_value'][1:-1])

                        if isinstance(arg['argument_value'], str):
                            if arg['argument_value'].strip()[0] == '{' and arg['argument_value'].strip()[-1] == '}':
                                arg['argument_value'] = string_to_dict(arg['argument_value'][1:-1])

                if arg['argument_value'] == 'true':
                    arg['argument_value'] = True
                if arg['argument_value'] == 'false':
                    arg['argument_value'] = False

    toolset_filename = 'hallucination.json'
    toolset_file = open(toolset_filename)
    toolset_data = json.load(toolset_file)
    toolset_ans = toolset_data['answer']

    calculate_metrics(toolset_ans , pred_ans , exp_ans)
