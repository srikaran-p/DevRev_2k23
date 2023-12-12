import json


def get_response(query,tools,chain):
    
    input = {
        'question':query,
        'tools':json.dumps(tools)
    }
    res = {
        'question':query,
        'answer': ""
    }

    try:
        output = chain.invoke(input)
        try:
            res['answer'] = json.loads(output['text'])
        except:
            res['answer'] = output['text']

    except Exception as e:
        print(e)
        return False,res
    
    return True, res