import json

def prompt_template_single_query(model_name, tools, query):
    if model_name=="mistral" or model_name=="llama" or model_name=="orca":
        return f"### Instructions:\n  Based on given API documentation {json.dumps(tools)} generate API call for following question To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i = 0, 1, .. j-1; j = current tool\u2019s index in the array If the query could not be answered with the given set of tools, output an empty list instead. ###{query}\n\n### Response:"
    elif model_name=="mistral_8x":
        return f"<s>[INST]\n Based on given API documentation {json.dumps(tools)} generate API call for following question To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i = 0, 1, .. j-1; j = current tool\u2019s index in the array If the query could not be answered with the given set of tools, output an empty list instead. ###{query}\n\n [/INST]### Response:"
    else:
        Exception("Model name not supported choose from mistral, llama, mistral_8x")
    
def prompt_template_batch(model_name, query):
    if model_name=="mistral" or model_name=="llama" or model_name=="orca":
        return f"### Instructions:\n{query}\n\n### Response:"
    elif model_name=="mistral_8x":
        return f"<s>[INST]\n{query}\n\n [/INST]### Response:"
    else:
        Exception("Model name not supported choose from mistral, llama, mistral_8x")