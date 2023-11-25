# **Zero Shot Pipeline with GPT-4 and GPT-3.5-turbo**

## **Setup**

1. Install pytorch
    ~~~
    $ conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
    ~~~
    or 
    ~~~
    $ pip3 install torch torchvision torchaudio
    ~~~
2. Install the requirements
    ~~~
    $ pip install -r requirements.txt
    ~~~
3. Setup the environment varibales
    - Add the following line in .env file
        ~~~
        OPENAI_API_KEY = <enter openai key>
        ~~~
4. Update the paths in `config.py`
    ~~~
    EXAMPLE_PATH      = "../data/example.json"
    FORMAT_PATH       = "../data/format.json"
    TOOLS_PATH        = "../data/tools.json"
    TOKEN_USAGE_PATH  = "../token_usage.txt"
    ~~~

## **Usage**

~~~
usage: main.py [-h] [-m [{gpt-4,gpt-3.5-turbo}]] [-n [{0,1,2,3}]] [-i [INPUT_TEST_PATH]]
               [-o [OUTPUT_FILE]] [-t [GET_TOKEN_USAGE]]

options:
  -h, --help            show this help message and exit
  -m [{gpt-4,gpt-3.5-turbo}], --model [{gpt-4,gpt-3.5-turbo}]
                        Choose the model (Default gpt-3.5-turbo)
  -n [{0,1,2,3}], --num_examples [{0,1,2,3}]
                        Number of Examples to pass in the prompt (Examples are predefined)
  -i [INPUT_TEST_PATH], --input_test_path [INPUT_TEST_PATH]
                        Path of the testcase file (Should be a csv file) (Deafult Terminal)
  -o [OUTPUT_FILE], --output_file [OUTPUT_FILE]
                        Location of output file to write the response (Default terminal)
  -t [GET_TOKEN_USAGE], --get_token_usage [GET_TOKEN_USAGE]
                        Get the token usage
~~~

### **Example**
~~~
python main.py -m gpt-4 -n 1 -i ../data/test_data.csv -o ../output/prediction.json
~~~

## **Instructions**
- Input file format:

    - Input file should be a csv with three fields ("id","query_type", "question")

- Tools Augumentation:
    
    - Add the tool details in the `tools.json`

- Token Usage Display:

    - Mention the file name in the `config.py`. 
    - if path is incorrect, it will not display.
