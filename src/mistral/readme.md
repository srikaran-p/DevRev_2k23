## Training


## Inference
In current inference pipeline we have to models
- mistral
- mistral-8x

### For inference
`import inference

checkpoint_path = "<model checkpoint path>"
model_name = "<mistral or mistral_8x>"
gpu_id = "<specify gpu id>"  #default value is 0


model = inference.init_model(checkpoint_path,gpu_id)
tokenizer = inference.init_tokenizer(checkpoint_path)

query = "<user query>"

#### tool documentation should be in json format, with list of tools, where each tool is a dictionary containing information like tool name, tool description, argument name, type and description
tools = "<tools description>" it should be json object

responce = inference.get_responce(model, tokenizer, query = query, tools = tools, model_name = model_name, gpu_id = gpu_id) # return type json object
`