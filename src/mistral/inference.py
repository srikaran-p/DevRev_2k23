from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import argparse
import json

from prompt_templates import prompt_template_single_query, prompt_template_batch
from tqdm import tqdm
from postprocessing import postprocess


import warnings
warnings.filterwarnings("ignore")

IGNORE_INDEX = -100
DEFAULT_PAD_TOKEN = "<|pad|>"
DEFAULT_EOS_TOKEN = "<|endoftext|>"
DEFAULT_UNK_TOKEN = "<|unk|>"

def init_model(checkpoint_path, gpu_id=0):
    return AutoModelForCausalLM.from_pretrained(checkpoint_path, use_auth_token=os.environ["HF_TOKEN"], torch_dtype=torch.bfloat16,).to(gpu_id)

def init_tokenizer(checkpoint_path):
    return AutoTokenizer.from_pretrained(checkpoint_path, model_max_length=3100, padding_side="right", use_fast=False, pad_token=DEFAULT_PAD_TOKEN, use_auth_token=os.environ["HF_TOKEN"], trust_remote_code=True,)

def get_response(model, tokenizer, query, tools, model_name="mistral_8x", gpu_id=0):
    prompt = prompt_template_single_query(model_name=model_name, query=query, tools=tools)
    encoded_prompt = tokenizer(prompt, return_tensors="pt", padding=False, max_length=tokenizer.model_max_length, truncation=True)
    generated_output = model.generate(encoded_prompt.input_ids.to(gpu_id), max_length=3100, do_sample=False)
    generated_output = tokenizer.batch_decode(generated_output, skip_special_tokens=False)
    if(postprocess(generated_output[0]) is not None):
        try:
            responce = json.dumps(json.loads(postprocess(generated_output[0]))[0])
        except:
            responce = []
    else:
        responce = []
    return {"question": query, "answer": responce}