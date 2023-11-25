from prompt import generate_promt
import helper
import config
import json
import os

from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# if key is wrong report error
def get_response(queries,model_name,num_examples):
    
    prompt = generate_promt(num_examples)
    if (num_examples > 0):
        examples = open(config.EXAMPLE_PATH,"r").read()
        examples = json.loads(examples)
    format = open(config.FORMAT_PATH,"r").read()
    tools = open(config.TOOLS_PATH,"r").read()
    
    
    chain = LLMChain(llm = ChatOpenAI(model=model_name), prompt=prompt)
    
    responses = []
    file = open(config.TOKEN_PATH,'a')
    file.write("\nUSE:{} {} examples\n".format(model_name,str(num_examples)))
    for idx, query in enumerate(queries):
        print("\r\fProcessing Query {}/{}".format(idx+1,len(queries)),end="")
        input = {
            'question':query,
            'tools':tools,
            'format':format
        }
        
        for i in range(num_examples):
            input["example"+str(i+1)] = examples[i]
        try:
            with get_openai_callback() as cb:
                output = chain.invoke(input)
                file.write(str(cb)+'\n\n')
        except Exception as e:
            raise Exception("Key is not correct")
            
        res = {
            'question_id': idx+1,
            'question':query,
            'answer': helper.filter(output)
        }
        responses.append(res)
    
    file.close()
    print("\nFinished Processing")
    return responses