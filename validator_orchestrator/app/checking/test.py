import sys
sys.path.append("../../") # go to parent dir

import requests
from app.checking.checking_functions import get_chat_data_validator_response, check_text_result, get_chat_data_response, check_text_result
import json
import httpx
from pydantic import BaseModel
from typing import Dict, Union, Optional, Any, List
import glob

class QueryResult(BaseModel):
    formatted_response: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]
    axon_uid: Optional[int]
    response_time: Optional[float]
    error_message: Optional[str]
    failed_axon_uids: List[int] = []

url = 'http://localhost:13320/generate_text'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    "messages": [
        {
            "role": "user",
            "content": "Write a short paragraph to describe something about yourself"
        }
    ],
    "seed": 0,
    "temperature": 0.1,
    "max_tokens": 50,
    "number_of_logprobs": 5,
    "starting_assistant_message": True,
    "top_k": 5,
    "additionalProp1": {}
}

from asgiref.sync import async_to_sync


@async_to_sync
async def print_data(data):
    return await get_chat_data_response(endpoint=url, data=data)

# a = print_data(data)

# with open("test.json", "w") as f:
#     json.dump(a, f)


# Open the file in read mode
count = 0 
with open('test.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        data['messages'][0]['content'] = "Write a short paragraph to describe: " + line.strip()
        a = print_data(data)
        with open(f"test_data/{count}.json", "w") as f:
            json.dump(a, f)
        count += 1
# # Write to a jsonl file
# with open('data_test.jsonl', 'w') as file:
#     for entry in list_valid:
#         # Convert the dictionary to a JSON string and write it to the file
#         file.write(json.dumps(entry) + '\n')
