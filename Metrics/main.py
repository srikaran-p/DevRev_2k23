from evaluationMetrics import Metrics
import json

m = Metrics()

file1 = open("../Dataset/halucination.json","r")

actual = json.loads(file1.read())

file2 = open("../test/zero_shot_three_examples/gpt-3.5-turbo.json","r")

predicted = json.loads(file2.read())

total = len(actual)

correct= 0
for p in predicted:
    

    try:
        if p['answer'] != [] :
            correct = correct + 1.0/(m.hallucination_rate(actual['answer'],p['answer']))
                
    except:
        pass
    # if (a['answer'] == [] and p['answer'] == []):
    #     correct += 1
print(total/correct)
    
