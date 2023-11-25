from prompt import generate_promt
import helper
import config
import json
import os
import time

from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# if key is wrong report error
def get_response(queries,model_name,num_examples,display_usage):
    
    #Prompt generation
    prompt = generate_promt(num_examples)
    if (num_examples > 0):
        examples = open(config.EXAMPLE_PATH,"r").read()
        examples = json.loads(examples)
    format = open(config.FORMAT_PATH,"r").read()
    tools = open(config.TOOLS_PATH,"r").read()
    
    # Intialization
    chain = LLMChain(llm = ChatOpenAI(model=model_name), prompt=prompt)
    
    if (display_usage):
        try:
            file = open(config.TOKEN_PATH,"w")
            file.write("USE: "+ model_name + str(num_examples) + " Examples")
        except:
            print("Token Path does not exists")
            display_usage = False
            
    # Updation
    responses = []
    for idx, query in enumerate(queries):
        
        # Number of token per min is limited
        if (model_name == "gpt-4" ):
            if (idx!=0 and idx%2 == 0):
                time.sleep(60)
        
        # Process input data with prompt
        print("\rProcessing Query {}/{}".format(idx+1,len(queries)),end="")
        input = {
            'question':query["question"],
            'tools':tools,
            'format':format
        }
        
        # Add examples
        for i in range(num_examples):
            input["example"+str(i+1)] = examples[i]
        
        # Ask LLM
        try:
            with get_openai_callback() as cb:
                output = chain.invoke(input)
                if (display_usage):
                    file.write(str(cb) + "\n")
        except Exception as e:
            print("\n",e)
            break
        
        # Generate Response
        res = {
            'id': query['id'],
            'query_type': query['query_type'],
            'question':query['question'],
            'answer': helper.filter(output['text'])
        }
        
        # Update 
        responses.append(res)
    
    
    print("\nFinished Processing")
    return responses