"""Grasshopper Script"""
# Simple QA of Large Language Models locally on Your Computer
# Copyright (C) 2024 Yan Peng <pydeoxy@gmail.com>

# This code is for a Python 3 Script component in Grasshopper with Rhino 8.
# To use this code, just copy the whole content into a Python 3 Script Script component,
# and to change the INPUTs and OUTPUTs according to the Args and Returns.
# Or, just use the llama_cpp.gh file.

# This componet is a simple example to run quantized LLMs with llama.cpp locally.
# More about llama.cpp, please see https://github.com/ggerganov/llama.cpp
# The LLMs used here are gguf models supported by llama.cpp
# To download gguf models, https://huggingface.co/models?library=gguf&sort=trending

"""
Simple QA of Large Language Models locally on Your Computer
    A simple example to run a QA funtion on llama.cpp with quantized LLMs  locally.

Args:
    loading: A boolean switch to load the LLM. Type: Boolean.
             It take a short moment to load the model. Switch this first.
             When loaded, 'out' info shows the details of the loaded model.
    execute: A boolean switch to run the QA. Type: Boolean.
             It take a longer moment to answer the question. 
             Please be prepared before switching the button.
             Better to turn it on after the question is ready.
             And be patient after click the button. :-)
    llm_model: Location of your local LLM model. Type: String.
             A gguf model supported by llama.cpp, for example:
             gemma-2b-it, https://huggingface.co/google/gemma-2b-it
             Llama-2-7B-Chat, https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
             Mistral-7B-Instruct, https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
    question: your own question to ask the LLM. Type: String.
    max_tokens: number of maximum tokens of the LLM's answer. Type: Integer.

Returns:
    answer: Answer from the LLM.

out:
    detail info of the loaded LLM.
    
"""

__author__ = "yan.peng"
__version__ = "2024.03.28"

from llama_cpp import Llama

# Load the Large Language Model(LLM).
path = llm_model
if loading:
    llm = Llama(model_path=path, n_gpu_layers=-1, n_ctx=2048, n_batch=512, verbose=True)

# Main QA function to get answer from LLM. 
if execute:
    output = llm(f"Q: {question} \nA:", max_tokens=max_tokens, echo=True)

# Print the answer.
    answer = output['choices'][0]['text']
