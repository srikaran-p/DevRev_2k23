from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate

from prompt import tool_summarize_template
import json
import config
import utils

def generate_summary(tool_json):

    if not utils.get_key():
        print("Error: OPENAI Key is not correct")
        return False,""
    
    prompt = PromptTemplate.from_template(tool_summarize_template)

    chain = LLMChain(llm = ChatOpenAI(model='gpt-3.5-turbo'), prompt=prompt)
    
    try:
        output = chain.invoke({'tools_json':tool_json})
        return True,output['text']
    
    except Exception as e:
        print("Error [Sumarize]: ",e)
        return False,""


def add_tool():

    tool_name = input("Enter tool_name: ")
    tool_description = input("Enter tool_description: ")

    arguments = []
    while True:
        argument_name = input("Enter argument name (or type 'done' to finish): ")
        if argument_name.lower() == 'done':
            break

        argument_type = input("Enter argument type: ")
        argument_description = input("Enter argument description: ")

        argument = {
            "name": argument_name,
            "type": argument_type,
            "description": argument_description
        }

        arguments.append(argument)

    tool = {
        "tool_name": tool_name,
        "tool_description": tool_description,
        "arguments": arguments
    }

    status,summary = generate_summary(tool)

    if not status:
        print("Unable to Generate Summary")
        return tool
    
    tool['summary'] = summary

    fp = open(config.TOOLS_PATH,'r')
    tools_json = json.load(fp)
    fp.close()

    tools_json.append(tool)

    fp = open(config.TOOLS_PATH,'w')
    json.dump(tools_json,fp,indent=4)
    fp.close()
    print("Added Successfully!!")
    return tool

    
def delete_tool():

    tool_name = input("Enter the tool name: ")

    fp = open(config.TOOLS_PATH,'r')
    tools_json = json.load(fp)
    fp.close()

    for i,tool in enumerate(tools_json):

        if (tool_name ==  tool['tool_name']):
            
            tools_json.pop(i)
            break
    else:
        print("Tool Not Found")
        return False
    fp = open(config.TOOLS_PATH,'w')
    json.dump(tools_json,fp,indent=4)
    fp.close()
    print("Deleted Successfully!!")
    return True


while True:
    print("\nMenu:")
    print("1. Add Tool")
    print("2. Remove Tool")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        add_tool()
    elif choice == '2':
        delete_tool()
    elif choice == '3':
        print("Exiting the program...")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")