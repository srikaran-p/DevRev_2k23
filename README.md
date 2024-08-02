# Inter IIT 12.0: DevRev - AI Agent 007: Tooling up for Success (TaskFlowAI)

As Large Language Models have become an integral part
of our lives, aiding us in nearly every sphere of our every-
day routines. From ChatGPT to LLaMa and Bard, numer-
ous models have been established that are breaking limits
in multiple fields. As the developments made using LLMs
are breaking ground at light year speed, the improvements
to LLMs are not very far behind. As a part of the High Prep
Statement: AI Agent 007: Tooling up for Success organized
by the Indian Institute of Technology, Madras, in collab-
oration with DevRev, we explore another improvement to
Large Language Models, arming the models with the power
to choose from a toolbox consisting of specific tools to help
answer queries. It has been shown that many of the tool-
augmented LLMs still mostly rely on closed LLM APIs. We
attempt to build on open-source LLMs with minimal human
intervention to achieve performance which is competitive
with closed LLMs. 

## Setup

Install the required dependencies using the following command:

`conda install --file env.yaml`


## API Key Configuration

1. Create a .env file in the project root directory.
2. Add your OpenAI API key and Hugging Face API key to the .env file as follows:

```
OPENAI_API_KEY="your_openai_api_key"
HF_TOKEN="your_hugging_face_api_key"
```

## How to Run

Use the main.py script to interact with the models. Here are the available options:

bash
usage: main.py [-h] [-m [{gpt-4,gpt-3.5-turbo,mistral,mistral_8x}]] [-i [INPUT_FILE]] [-o [OUTPUT_FILE]]

options:
  -h, --help            show this help message and exit
  -m [{gpt-4,gpt-3.5-turbo,mistral,mistral_8x}], --model [{gpt-4,gpt-3.5-turbo,mistral,mistral_8x}]
                        Choose the model (Default gpt-3.5-turbo)
  -i [INPUT_FILE], --input_file [INPUT_FILE]
                        Location of input file to read the query (Default terminal)
  -o [OUTPUT_FILE], --output_file [OUTPUT_FILE]
                        Location of output file to write the response (Default terminal)


### Example

Run the following command to use the script:

bash
python main.py -m [model] -i [input_file] -o [output_file]


## Configuration
# Configuration

This section outlines the configuration parameters used in the project. Modify these settings as needed.

## Paths

### TRAIN_PATH

This parameter specifies the location of the training data in JSON format. Update the path accordingly.

python
TRAIN_PATH = "../data/train_data.json"


### TOOLS_PATH

The TOOLS_PATH parameter defines the path to the JSON file containing tools information.

python
TOOLS_PATH = "../tool/tools.json"


## Model Checkpoints

Download the model checkpoints from the provided Google Drive link and update the paths accordingly.

### RETRIEVER_CHECKPOINT

This checkpoint is used for the summarizer retriever.

python

### DOWNLOAD FROM GOOGLE DRIVE LINK PROVIDED IN REPORT


RETRIEVER_CHECKPOINT = "../checkpoints/checkpoint_summarizer"


### MISTRAL_CHECKPOINT (will be downloaded from huggingface automatically)


The Mistral model checkpoint is specified here.

python
MISTRAL_CHECKPOINT = "../checkpoints/checkpoint_summarize"


### MISTRAL_8X_CHECKPOINT

This checkpoint is for the Mistral model with 8x summarization capability.

python
MISTRAL_8X_CHECKPOINT = "../checkpoints/checkpoint_summarier"


## Download Model Checkpoints

You can download the required model checkpoints from the provided Google Drive link [here](https://drive.google.com/drive/folders/1D16dWzdulKp0XItxg8fiMiFbM3e_Cqje?usp=sharing). Place the downloaded checkpoints in the corresponding paths mentioned above.

Make sure to keep the directory structure intact for the proper functioning of the project.

## Edit Tools
### LangChain Tool Manager

This is a simple tool manager script using LangChain, which leverages OpenAI's GPT-3.5 Turbo model for summarizing tools.

### Installation

Before running the script, make sure you have the required dependencies installed. You can install them using the following:

bash
pip install langchain prompt_toolkit


### Configuration

Ensure that you have a valid OpenAI API key configured. Add the key to the config.py file.

### Usage

Run the script using the following command:

bash
python your_script_name.py


The script presents a menu with the following options:

1. *Add Tool:* Allows you to add a new tool with its name, description, and arguments.

2. *Remove Tool:* Lets you delete a tool by specifying its name.

3. *Exit:* Exits the program.

### Sample Tool Addition

When adding a tool, you'll be prompted to provide the tool's name, description, and a list of arguments. The tool summary is generated using LangChain's summarization capabilities.

### Note

- Make sure to handle the OpenAI API key correctly; otherwise, the script won't function properly.
- The tools are stored in a JSON file specified in the config.py file.

## Contributors
- [Shrey Satapara](https://shreysatapara.github.io)
- [Anirudh Srinivasan](https://www.linkedin.com/in/anirudh-srini/)
- [Harsh Goyal](https://www.linkedin.com/in/harsh-goyal-441a06243/)
- [Srikaran P](https://www.linkedin.com/in/srikaran-p-b82221214/)
- [Arsh Arora](https://www.linkedin.com/in/arsh-arora/)
- [Ayush Kumar Singh](https://www.linkedin.com/in/ayush-kumar-singh-272a471b9/)
- R Raghuveer
- [Tanmay Goyal](https://www.linkedin.com/in/tanmay-goyal-57253a213/)
- Vaishnai
