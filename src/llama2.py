from prompt import generate_promt
import config
import helper
import json

from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer
from langchain.chains import ConversationChain
import transformers
import torch
from langchain.chains import LLMChain

def get_response(queries,model_name,num_examples):
    prompt = generate_promt(num_examples)
    if (num_examples > 0):
        examples = open(config.EXAMPLE_PATH,"r").read()
        examples = json.loads(examples)
    format = open(config.FORMAT_PATH,"r").read()
    tools = open(config.TOOLS_PATH,"r").read()
    
    # model=config.MODEL_PATH+model_name
    model = "togethercomputer/Llama-2-7B-32K-Instruct"
    tokenizer=AutoTokenizer.from_pretrained(model)
    pipeline=transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_length=3000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
    )

    llm=HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature':0.7})

    
    chain = LLMChain(llm=llm, prompt=prompt)
    responses = []
    
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
            
            output = chain.invoke(input)
            
        except Exception as e:
            raise Exception("Key is not correct")
            
        res = {
            'question_id': idx+1,
            'question':query,
            'answer': helper.filter(output['text'])
        }
        responses.append(res)
    
    print("\nFinished Processing")
    return responses