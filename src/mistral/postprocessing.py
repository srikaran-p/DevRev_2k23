import json
import re

def postprocess(text):

# Define the pattern to match the content between ### Response: and </s>
    pattern = re.compile(r'### Response:(.*?)<\/s>', re.DOTALL)

# Find all matches in the given string
    matches = re.findall(pattern, text)

# Print the extracted content
    if(matches[0] == '[]'):
        return None
    return matches[0].strip()
