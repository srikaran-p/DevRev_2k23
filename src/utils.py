import sys
import os
import dotenv
import openai
import json

def get_query(input_path):

    file = open(input_path,"r")
    queries = file.read().split('\n')
    
    return queries

def get_input(input_file):
    
    # if input is stdin
    if (input_file == sys.stdin):
        queries = [input("Enter the query: ")]  # Query
    # if input path do not exists
    elif not (os.path.exists(input_file)):
        print("Error: Input Path does not exist")
        return False,[]
    # if input path is a directory
    elif (os.path.isdir(input_file)):
        print("Error: Input Path is a directory")
        return False,[]
    else:
        # get queries from the file
        queries = get_query(input_file)
    
    # left of query or empty query is given, exit
    if len(queries) == 0 or not queries[0]:
        print("No query Provided")
        return False,[]
    
    return True, queries

def is_api_key_valid():
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
    except:
        return False
    else:
        return True
    
def get_key():

    # Load the key 
    dotenv.load_dotenv()
    
    # if key in not loaded, ask for key
    if not (os.getenv('OPENAI_API_KEY')):
        key = input("Enter key:")
        os.environ['OPENAI_API_KEY'] = key
    
    if is_api_key_valid():
        return True
    else:
        return False

def write_output(output_file,response):

    # if output is stdout
    if (output_file == sys.stdout):
        output = output_file
        
    # if output is not a directory, file name given
    elif not (os.path.isdir(output_file)):
        output = open(output_file + ".json","w")
        
    # if output path does not exists
    elif not (os.path.exists(output_file)):
        
        os.mkdir(output_file)
        output = open(os.path.join(output_file,"output.json"),"w")
        print("Created ",output_file)
        
    # if output is directory, generate model_name.json
    else:
        output = open(os.path.join(output_file,"output.json"),"w")
    
    try:
        output.write(json.dumps(response))
    except:
        return False
    else:
        output.close()
        return True
    