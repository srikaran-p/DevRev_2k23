from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate

from prompt import tool_summarize_template

def generate_summary(tool_json):

    prompt = PromptTemplate(tool_summarize_template)

    chain = LLMChain(llm = ChatOpenAI(model='gpt-3.5-turbo'), prompt=prompt)
    try:
        output = chain.invoke({'tool_json':tool_json})
        tool_json['summary'] = output['text']
    except Exception as e:
        print("Sumarize: ",e)
        tool_json['summary'] = ""

    return tool_json
