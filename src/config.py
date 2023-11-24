
EXAMPLE_PATH = "../json/example.json"
FORMAT_PATH = "../json/format.json"
TOOLS_PATH = "../json/tools.json"
TOKEN_PATH = "../config/token.txt"

# key check (else error)
def get_key(key_path):
    
    key = open(key_path,"r").read().splitlines()[0]
    return key