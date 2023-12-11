import argparse
import os
import gpt
import sys
import dotenv
import IR_model

def main():
    parser = argparse.ArgumentParser()
    
    # Model Name
    parser.add_argument(
        '-m',
        "--model",
        choices=["gpt-4","gpt-3.5-turbo"],
        help="Choose the model (Default gpt-3.5-turbo)",
        nargs="?",
        default="gpt-3.5-turbo"
    )

    # Output Path of Test Cases
    parser.add_argument(
        '-o',
        "--output_file",
        nargs="?",
        help="Location of output file to write the response (Default terminal)",
        default=sys.stdout,
    )
    
    args = parser.parse_args()

    # if input is stdin
    if (args.input_test_path == sys.stdin):
        q = input("Enter the query: ")  # Query
        query = {
            "question":q
        }
    
    # left of query or empty query is given, exit
    if  not query['question']:
        print("No query Provided")
        return False
    
    # Load the key 
    dotenv.load_dotenv()
    
    # if key in not loaded, ask for key
    if not (os.getenv('OPENAI_API_KEY')):
        key = input("Enter key:")
        # if key not given, exits
        if not key:
            print("Error: No Key Provided")
            return False
        else:
            os.environ['OPENAI_API_KEY'] = key
    
    # Generate Relevant tools based on query
    relevant_tools = IR_model.get_relevant_tools(query['question'])

    # Get the responses 
    response = gpt.get_response(query,relevant_tools,args.model)

    # if output is stdout
    if (args.output_file == sys.stdout):
        output = args.output_file
        
    # if output is not a directory, file name given
    elif not (os.path.isdir(args.output_file)):
        output = open(args.output_file + ".json","w")
        
    # if output path does not exists
    elif not (os.path.exists(args.output_file)):
        
        os.mkdir(args.output_file)
        output = open(os.path.join(args.output_file,args.model + ".json"),"w")
        print("Created ",args.output_file)
        
    # if output is directory, generate model_name.json
    else:
        output = open(os.path.join(args.output_file,args.model + ".json"),"w")
    
    output.write(response)
    
    output.close()
    return True

if __name__ == "__main__":
    main()