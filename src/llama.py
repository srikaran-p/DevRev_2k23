from transformers import LlamaForCausalLM, LlamaTokenizer
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
import transformers
from langchain.llms import HuggingFacePipeline
import json
import random

example_file = open("../json/example.json","r")
test_file = open("../json/test.json","r")
format = open("../json/format.json","r").read()
tools = open("../json/tools.json","r").read()

# get examples
test_examples = json.loads(test_file.read())
examples = json.loads(example_file.read())

prompt_template= """
{tools_template}

{format_template}

{example_template}

{start_template}
"""

tools_template = """
Use the following tools and answer the given question using given answer format, 
{tools}
"""
answer_format_template = """
Generated answer for any given question should have following format
{format}
"""

example_template = """
Following are the example of question-answer pairs for the abovementioned tools
Example 1
{example1}

Example 2
{example2}
"""

start_template = """
To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i = 0, 1, .. j-1; j = current tool’s index in the array
If the query could not be answered with the given set of tools, output an empty list instead.

Empty list should look like []. Whenever you want to access information about current user to pass it further, you need to make a call to whoami api tool.

Answer the following question based on instructions provided above.
question: {question}
answer:{{
"question":
"answer":
}}"""

full_prompt = PromptTemplate.from_template(prompt_template)
tools_prompt = PromptTemplate.from_template(tools_template)
answer_format_prompt = PromptTemplate.from_template(answer_format_template)
example_prompt = PromptTemplate.from_template(example_template)
start_prompt = PromptTemplate.from_template(start_template)

input_prompt = [
    ("tools_template",tools_prompt),
    ("format_template",answer_format_prompt),
    ("example_template",example_prompt),
    ("start_template",start_prompt)
]
prompt = PipelinePromptTemplate(final_prompt=full_prompt,pipeline_prompts=input_prompt)
print(prompt.input_variables)


model_path = "../models/CodeLlama/Codellama7B/"

# tokenizer = LlamaTokenizer.from_pretrained(model_path)
# model = LlamaForCausalLM.from_pretrained(model_path)

# generate_text = transformers.pipeline(
#     model=model, 
#     tokenizer=tokenizer,
#     return_full_text=True,  # langchain expects the full text
#     task='text-generation',
#     # we pass model parameters here too
#     temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
#     max_new_tokens=4096,  # max number of tokens to generate in the output
#     repetition_penalty=1.1  # without this output begins repeating
# )
# llm = HuggingFacePipeline(pipeline=generate_text)
# # chain = LLMChain(llm = model, prompt=prompt)
# for test in test_examples:

#     if (test['question_id'] == '2'):
#         continue
#     print(test['question_id'])
#     # input = prompt.format(question=test['question'],tools=tools,format=format,examples=examples)
#     output = llm(prompt = prompt.format(question=test['question'],tools=tools,format=format,example1=examples[0],example2=examples[1]))
#     break

from langchain.llms import LlamaCpp
from langchain.chains import LLMChain

llm = LlamaCpp(model_path=model_path,n_ctx=4096)
# chain = LLMChain(llm = ChatOpenAI(model='gpt-4'), prompt=prompt)
chain = LLMChain(llm = llm, prompt=prompt)

output = chain.invoke({'question':test_examples[1]['question'],'tools':tools,'format':format,'example1':examples[0],'example2':examples[1]})


file = open("../output/test1.json","w")
file.write(output)
file.close()
file = open("../output/test2.json","w")
file.write(json.dumps(output))
file.close()