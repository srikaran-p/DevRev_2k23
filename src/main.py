import argparse
import gpt
import sys
import IR_model
import utils
import prompt
import time

sys.path.insert(1,'mistral')
import inference

import config

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate

def main():
    parser = argparse.ArgumentParser()
    
    # Model Name
    parser.add_argument(
        '-m',
        "--model",
        choices=["gpt-4","gpt-3.5-turbo","mistral","mistral_8x"],
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

    # Load the IR Model
    retreiver,ranker,ranker_documents_embed,documents = IR_model.load_model()
    print("IR Checkpoint Loaded\n")

    status,queries = utils.get_input(args.input_file)
    if not status:
        return False
    
    # Output
    response = []

    # GPT
    if args.model == "gpt-4" or args.model == "gpt-3.5-turbo":

        if not utils.get_key():
            print("Error: OPENAI Key is not correct")
            return False


        p = PromptTemplate.from_template(prompt.gpt_inference_template)
        chain = LLMChain(llm=ChatOpenAI(model= args.model), prompt=p)
        for query in queries:

            start_time = time.time()
            relevant_tools = IR_model.get_relevant_tools(query,retreiver,ranker,ranker_documents_embed,documents)
            status,res = gpt.get_response(query,relevant_tools,chain)
            end_time = time.time()
            if not status:
                print("Error [GPT]: Unable to generate answer")
                break
            
            res['Inference Time'] = end_time-start_time
            response.append(res)
    
    elif args.model == "mistral" or args.model == "mistral-8x":
        try:
            gpu_id = int(input("Enter the GPU Id to run the model(For eg: '0'): "))
        except:
            print("Incorrect GPU id")
            return False
        
        if (gpu_id < 0):
            return False
        
        # Load Mistral
        try:
            if (args.model == "mistral"):
                model = inference.init_model(config.MISTRAL_CHECKPOINT,gpu_id)
                tokenizer = inference.init_tokenizer(config.MISTRAL_CHECKPOINT,gpu_id)

            else:
                model = inference.init_model(config.MISTRAL_8X_CHECKPOINT,gpu_id)
                tokenizer = inference.init_tokenizer(config.MISTRAL_8X_CHECKPOINT,gpu_id)

        except Exception as e:
            print(e)
            print("Error in loading the model")
            return False

        for query in queries:

            start_time = time.time()
            relevant_tools = IR_model.get_relevant_tools(query)
            res = inference.get_response(model,tokenizer,query,relevant_tools,gpu_id)
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