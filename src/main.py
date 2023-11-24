import argparse
import os
import helper
import llama2
import gpt
import config
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        "--model",
        choices=["gpt-4","gpt-3.5-turbo","llama-7b-chat","llama-13b-chat","codellama-7b","codellama-13b","codellama-7b-instruct","codellama-13b-instruct"],
        help="Choose the model to use for testing",
        required=True
    )
    parser.add_argument(
        '-k',
        "--key_path",
        nargs="?",
        help="Location of key (if using GPTs)",
        default=sys.stdin
    )
    parser.add_argument(
        '-n',
        "--num_examples",
        choices=[0,1,2,3],
        help="Number of Examples to pass in the prompt (Examples are predefined)",
        type=int,
        required=True
    )
    parser.add_argument(
        '-i',
        "--input_test_path",
        nargs="?",
        help="Location of Test case file (Follow the structure of Test cases provided in the docs) ",
        default=sys.stdin
    )

    parser.add_argument(
        '-o',
        "--output_file",
        nargs="?",
        help="Location of output file to write the response ",
        default=sys.stdout,
    )
    args = parser.parse_args()

    if (args.input_test_path == sys.stdin):
        query = [input("Enter the query: ")]
    elif not (os.path.exists(args.input_test_path)):
        print("Error: Input Path does not exist")
        return False
    elif (os.path.isdir(args.input_test_path)):
        print("Error: Input Path is a directory")
        return False
    else:
        query = helper.get_list_of_query(args.input_test_path)
    

    if len(query) == 0 or not query[0]:
        print("No query Provided")
        return False
    if (args.key_path == sys.stdin):
        key = input("Enter key: ")
    else:
        key = config.get_key(args.key_path)
    if not key:
        print("Error: No Key Provided")
        return False
        
    if ("gpt" in args.model):
        response = gpt.get_response(query,args.model,key,args.num_examples)
        
    elif ("llama" in args.model):
        response = llama2.get_response(query,args.model,args.num_examples)
    
    if (args.output_file == sys.stdout):
        output = args.output_file
    elif not (os.path.isdir(args.output_file)):
        output = open(args.output_file + ".json","w")
    else:
        output = open(os.path.join(args.output_file,args.model + ".json"),"w")
    
    if not (helper.write_output(output,response)):
        return False
    output.close()
    return True

if __name__ == "__main__":
    main()