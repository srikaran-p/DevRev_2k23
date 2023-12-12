import argparse
import gpt
import sys
import IR_model
import utils
import prompt
import mistral
import time

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate

def main():
    parser = argparse.ArgumentParser()
    
    # Model Name
    parser.add_argument(
        '-m',
        "--model",
        choices=["gpt-4","gpt-3.5-turbo","mistral","mistral-8x"],
        help="Choose the model (Default gpt-3.5-turbo)",
        nargs="?",
        default="gpt-3.5-turbo"
    )
    # Input path
    parser.add_argument(
        '-i',
        "--input_file",
        nargs="?",
        help="Location of input file to read the query (Default terminal)",
        default=sys.stdin,
    )
    # Output Path 
    parser.add_argument(
        '-o',
        "--output_file",
        nargs="?",
        help="Location of output file to write the response (Default terminal)",
        default=sys.stdout,
    )
    
    args = parser.parse_args()

    status,queries = utils.get_input(args.input_file)
    if not status:
        return False
    
    # Load the IR Model [?]

    # Output
    response = []

    # GPT
    if args.model == "gpt-4" or args.model == "gpt-3.5-turbo":

        if not utils.get_key():
            print("Error: OPENAI Key is not correct")
            return False

        p = PromptTemplate(prompt.gpt_inference_template)
        chain = LLMChain(llm=ChatOpenAI(model= args.model), prompt=p)

        for query in queries:

            start_time = time.time()
            relevant_tools = IR_model.get_relevant_tools(query)
            status,res = gpt.get_response(query,relevant_tools,chain)
            end_time = time.time()
            if not status:
                print("Error [GPT]: Unable to generate answer")
                break
            
            res['Inference Time'] = end_time-start_time
            response.append(res)
    
    elif args.model == "mistral" or args.model == "mistral-8x":

        # Load Mistral [?]

        for query in queries:

            start_time = time.time()
            relevant_tools = IR_model.get_relevant_tools(query)
            res = mistral.get_response(query,relevant_tools)
            end_time = time.time()

            res['Inference Time'] = end_time-start_time
            response.append(res)


    status = utils.write_output(args.output_file,response)
    if not status:
        print("Error: Unable to Write in Output File")
        print(response)
        return False

    return True

if __name__ == "__main__":
    main()