import json
import csv
def get_query(input_path):

    # Load csfile
    csvfile = open(input_path,"r")
    
    queries = []
    fieldnames = ("id","query_type","question")
    
    try:
        reader = csv.DictReader(csvfile,fieldnames)
    except:
        print("Unable to load file")
        return []
    
    # appending queries
    for row in reader:
        queries.append(row)
    
    return queries[1:]
    

def write_output(output_file,responses):
    
    # check if the file can be written on output file
    try:
        json.dump(responses,output_file,indent=4)
        output_file.write('\n')
        return True
    except:
        # print the responses on terminal if can not be written
        print("Error: Unable to Write on output_file")
        print("Responses are \n",responses)
        return False


def filter(output):
    # if output can be converted into json, else return output as it is.
    try:
        ans = json.loads(output)
    except:
        ans = output
    
    return ans