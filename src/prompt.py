
gpt_inference_template = '''
Use the following tools and answer the given question using given answer format, 
{tools}

Generated answer for any given question should have following format
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "tool_name": {{ "type": "string" }},
            "arguments": {{
                "type": "array",
                "items": {{
                    "type": "object",
                    "properties": {{
                        "argument_name": {{ "type": "string" }},
                        "argument_value": {{ "type": "string" }}
                    }},
                    "required": ["argument_name", "argument_value"]
                }}
            }}
        }},
        "required": ["tool_name", "arguments"]
    }}
}}

Following are the example of question-answer pairs for the above mentioned tools
Example 1
{{
    "question":"Summarize issues similar to don:core:dvrv-us-1:devo/0:issue/1",
    "answer":[
        {{
            "tool_name": "get_similar_work_items",
            "arguments": [
                {{
                    "argument_name": "work_id",
                    "argument_value": "don:core:dvrv-us-1:devo/0:issue/1"
                }}
            ]
        }},
        {{
            "tool_name": "summarize_objects",
            "arguments": [
                {{
                    "argument_name": "objects",
                    "argument_value": "$$PREV[0]"
                }}
            ]
        }}
    ]
}}

Example 2
{{
        
    "question":"Summarize high severity tickets from the customer UltimateCustomer",
    "answer":[
        {{
            "tool_name": "search_object_by_name",
            "arguments": [
                {{
                "argument_name": "query",
                "argument_value": "UltimateCustomer"
                }}
            ]
        }},
        {{
            "tool_name": "works_list",
            "arguments": [
                {{
                    "argument_name": "ticket.rev_org",
                    "argument_value": ["$$PREV[0]"]
                }},
                {{
                    "argument_name": "ticket.severity",
                    "argument_value": ["high"]
                }},
                {{
                    "argument_name": "type",
                    "argument_value": ["ticket"]
                }}
            ]
        }},
        {{
            "tool_name": "summarize_objects",
            "arguments": [
                {{
                    "argument_name": "objects",
                    "argument_value": "$$PREV[1]"
                }}
            ]
        }}
    ]
}}

To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i = 0, 1, .. j-1; j = current tool’s index in the array
If the query could not be answered with the given set of tools, output an empty list instead.

Empty list should look like []. Whenever you want to access information about current user to pass it further, you need to make a call to whoami api tool.

Answer the following question based on instructions provided above.
question: {question}
answer:
'''

tool_summarize_template = '''
{tools_json}

Given above tool that contains tool with required arguments and their description, generated a brief summary what that tool can do

Do not generate points. Generate single paragraph summary without any addtional text.

'''