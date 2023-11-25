import argparse
import os
import helper
import llama2
import gpt
import config
import sys
import dotenv

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
    
    # Number of Examples in the prompt
    parser.add_argument(
        '-n',
        "--num_examples",
        choices=[0,1,2,3],
        help="Number of Examples to pass in the prompt (Examples are predefined)",
        type=int,
        nargs="?",
        default=2
    )
    
    # Input Path of Test Cases
    parser.add_argument(
        '-i',
        "--input_test_path",
        nargs="?",
        help="Path of the testcase file (Should be a csv file) (Deafult Terminal)",
        default=sys.stdin
    )

    # Output Path of Test Cases
    parser.add_argument(
        '-o',
        "--output_file",
        nargs="?",
        help="Location of output file to write the response (Default terminal)",
        default=sys.stdout,
    )
    parser.add_argument(
        '-t',
        "--get_token_usage",
        nargs="?",
        help="Get the token usage",
        type = bool,
        default=False,
    )
    
    args = parser.parse_args()

    # if input is stdin
    if (args.input_test_path == sys.stdin):
        q = input("Enter the query: ")  # Query
        queries = [{
            "id":"test_data_0",
            "query_type":"zero_shot",
            "question":q
        }]
    # if input path do not exists
    elif not (os.path.exists(args.input_test_path)):
        print("Error: Input Path does not exist")
        return False
    # if input path is a directory
    elif (os.path.isdir(args.input_test_path)):
        print("Error: Input Path is a directory")
        return False
    else:
        # get queries from the file
        queries = helper.get_query(args.input_test_path)
    
    # left of query or empty query is given, exit
    if len(queries) == 0 or not queries[0]:
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
    
    # Get the responses 
    response = gpt.get_response(queries,args.model,args.num_examples,args.get_token_usage)

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
    
    
    # if it is unable to write at output path
    if not (helper.write_output(output,response)):
        return False
    
    output.close()
    return True

if __name__ == "__main__":
    main()