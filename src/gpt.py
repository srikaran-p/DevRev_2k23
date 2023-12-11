from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate

import time
from prompt import gpt_inference_template

# if key is wrong report error
def get_response(query,tools,model_name):
    
    #Prompt generation
    prompt = prompt = PromptTemplate(gpt_inference_template)

    # Intialization
    chain = LLMChain(llm = ChatOpenAI(model=model_name), prompt=prompt)
    
    # Updation
    responses = []
    
    input = {
        'question':query["question"],
        'tools':tools
    }
    
    try:
        output = chain.invoke(input)

    except Exception as e:
        print("GPT response: ",e)
        return []
    
    # Generate Response
    res = {
        'question':query['question'],
        'answer': output['text']
    }
    
    # Update 
    responses.append(res)
    
    return responses