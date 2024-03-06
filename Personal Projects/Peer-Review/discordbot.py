from datetime import datetime

import requests

API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query(
    {
        "inputs": {
            "question": "What is my location?",
            "context": "My name is Clara and I live in Berkeley.",
        },
    }
)

print(output)


# Get the current date and time
current_date = datetime.now()

# Specify the path for the text file
text_file_path = f"Peer Review {current_date.date()}.txt"

# Write "hello" to the text file
with open(text_file_path, "w") as text_file:
    text_file.write("test\n")
