import json
def get_list_of_query(input_path):
    
    return open(input_path,"r").read().splitlines()
    

def write_output(output_file,responses):
    
    try:
        json.dump(responses,output_file,indent=4)
        output_file.write('\n')
        return True
    except:
        print("Error: Unable to Write")
        print("Responses are \n",responses)
        return False

# Need to update this for general
def filter(output):
    # return json
    try:
        ans = json.loads(output)
    except:
        ans = output
    
    return ans