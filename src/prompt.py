from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate

from template import prompt_template, tools_template, answer_format_template, start_template
from template import generate_example_template



def generate_promt(num_examples):
    
    full_prompt = PromptTemplate.from_template(prompt_template)
    tools_prompt = PromptTemplate.from_template(tools_template)
    answer_format_prompt = PromptTemplate.from_template(answer_format_template)
    example_prompt = PromptTemplate.from_template(generate_example_template(num_examples))
    start_prompt = PromptTemplate.from_template(start_template)

    input_prompt = [
        ("tools_template",tools_prompt),
        ("format_template",answer_format_prompt),
        ("example_template",example_prompt),
        ("start_template",start_prompt)
    ]
    prompt = PipelinePromptTemplate(final_prompt=full_prompt,pipeline_prompts=input_prompt)
    return prompt