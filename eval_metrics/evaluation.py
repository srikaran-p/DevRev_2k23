import json

exp_file = open('all_mistral.json')

exp_data = json.load(exp_file)
#
# print(json.loads(exp_data[20]['generated_answer']))
# print(json.loads(exp_data[20]['actual_answer']))
# print(exp_data[0])
lol = {}
for exp in exp_data:
    # print(exp['example_type'])
    if exp['example_type'] in lol:
        lol[exp['example_type']] += 1
    else:
        lol[exp['example_type']] = 1

print(lol)
