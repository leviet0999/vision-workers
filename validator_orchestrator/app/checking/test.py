import sys
sys.path.append("../../") # go to parent dir

import requests
from app.checking.checking_functions import get_chat_data_validator_response
import json

url = 'http://localhost:11437/generate_text'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    "messages": [
        {
            "role": "user",
            "content": ""
        }
    ],
    "seed": 0,
    "temperature": 0.5,
    "max_tokens": 30,
    "number_of_logprobs": 1,
    "starting_assistant_message": True,
    "top_p": 1,
    "additionalProp1": {}
}

from asgiref.sync import async_to_sync

@async_to_sync
async def print_data(data):
    return await get_chat_data_validator_response(endpoint=url, data=data)


# Open the file in read mode
list_valid = []
with open('test.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        data['messages'][0]['content'] = "Write a short paragraph to describe: " + line.strip()
        a = print_data(data)
        list_valid.append(a)


# Write to a jsonl file
with open('data_test.jsonl', 'w') as file:
    for entry in list_valid:
        # Convert the dictionary to a JSON string and write it to the file
        file.write(json.dumps(entry) + '\n')
