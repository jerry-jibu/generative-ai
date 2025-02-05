import json
import os
import requests

INFERENCE_API_BASE_URL = "http://inference-api:5000"
INFERENCE_API_HEALTHCHECK_ENDPOINT_URL = f"{INFERENCE_API_BASE_URL}/api/health"
INFERENCE_API_GENERATION_ENDPOINT_URL = f"{INFERENCE_API_BASE_URL}/api/generate"
INFERENCE_API_GENERATION_STREAM_ENDPOINT_URL = f"{INFERENCE_API_BASE_URL}/api/generate_stream"
INFERENCE_API_COMPLETION_URL = f"{INFERENCE_API_BASE_URL}/api/generate_completion"
INFERENCE_API_CHAT_COMPLETION_URL = f"{INFERENCE_API_BASE_URL}/api/chat/generate"
INFERENCE_API_CHAT_COMPLETION_STREAM_URL = f"{INFERENCE_API_BASE_URL}/api/chat/generate_stream"

HEADERS = {
        "Content-Type":"application/json",
        "accept":"application/json"
    }

DEFAULT_GENERATION_PARAMS = {
        "max_new_tokens": 10,
        "repetition_penalty": 1,
        "do_sample": True,
        "top_p": 1,
        "top_k": 50,
        "typical_p": 1,
        "temperature": 0.5,
        "remove_tokens": [],
        "stop_sequences": [],
        "log_inferences": True
    }

def healthcheck(endpoint=INFERENCE_API_HEALTHCHECK_ENDPOINT_URL):
     res = requests.get(endpoint)
     if res.status_code == 200:
          return True
     else:
          return False

def generate_stream(input:str, generation_params = DEFAULT_GENERATION_PARAMS, endpoint=INFERENCE_API_GENERATION_STREAM_ENDPOINT_URL):
    
    data = dict(DEFAULT_GENERATION_PARAMS)
    data.update(generation_params)
    data["input"] = input

    with requests.post(url=endpoint, headers=HEADERS, data=json.dumps(data), stream=True) as r:
            for chunk in r.iter_lines(decode_unicode=True):
                yield json.loads(chunk.decode("utf8"))["text"]


def generate(input:str, generation_params = DEFAULT_GENERATION_PARAMS, endpoint=INFERENCE_API_GENERATION_ENDPOINT_URL):

    data = dict(generation_params)
    data["input"] = input

    res = requests.post(url=endpoint, headers=HEADERS, data=json.dumps(data))
    return res.json()

def create_completion(input:str, generation_params = None, endpoint=INFERENCE_API_COMPLETION_URL):
     
    if not generation_params:
        generation_params = {
        "max_tokens":500,
        "repeat_penalty":1.0,
        "top_p":1.0,
        "top_k":50,
        "typical_p":1.0,
        "temperature":0.7
        }
    data = {
        "input":input,
        "params":generation_params
    }
    res = requests.post(url=endpoint,headers=HEADERS,data=json.dumps(data))
    return res.json()

def create_chat_completion(messages:list[dict], generation_params = None, endpoint=INFERENCE_API_CHAT_COMPLETION_URL):
     
    if not generation_params:
        generation_params = {
        "max_tokens":500,
        "repeat_penalty":1.0,
        "top_p":1.0,
        "top_k":50,
        "typical_p":1.0,
        "temperature":0.7
        }
    data = {
        "messages":messages,
        "params":generation_params
    }
    res = requests.post(url=endpoint,headers=HEADERS,data=json.dumps(data))
    return res.json()