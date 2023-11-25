prompt_template= """
{tools_template}

{format_template}

{example_template}

{start_template}
"""

tools_template = """
Use the following tools and answer the given question using given answer format, 
{tools}
"""
answer_format_template = """
Generated answer for any given question should have following format
{format}
"""

example_template_with_no_examples = """
"""

example_template_with_one_example = """
Following are the example of question-answer pairs for the abovementioned tools
Example 1
{example1}
"""

example_template_with_two_examples = """
Following are the example of question-answer pairs for the abovementioned tools
Example 1
{example1}

Example 2
{example2}
"""

example_template_with_three_examples = """
Following are the example of question-answer pairs for the abovementioned tools
Example 1:
{example1}

Example 2:
{example2}

Whenver there is a need of finding current User api call to whoami is mandatory like following example

Example 3:
{example3}
"""

start_template = """
To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i = 0, 1, .. j-1; j = current tool’s index in the array
If the query could not be answered with the given set of tools, output an empty list instead.

Empty list should look like []. Whenever you want to access information about current user to pass it further, you need to make a call to whoami api tool.

Answer the following question based on instructions provided above.
question: {question}
answer:"""

def generate_example_template(num_example):
    if num_example == 0:
        return example_template_with_no_examples
    elif num_example == 1:
        return example_template_with_one_example
    elif num_example == 2:
        return example_template_with_two_examples
    elif num_example == 3:
        return example_template_with_three_examples