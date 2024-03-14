from datetime import datetime
import pandas as pd
import requests
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT = False

import requests

response = client.embeddings.create(
    model="text-embedding-ada-002", input="The food was delicious and the waiter..."
)

print(response)


data = pd.read_csv("LMU_Blue_peer_review_test.csv")
names = {"Chris", "Elijah", "Toby", "Mason", "Rei", "Viv"}

data_by_name = {}

for name in names:
    relevant_columns = [col for col in data.columns if name in col]

    data_for_name = {}
    for col in relevant_columns:
        data_for_name[col] = data[col].tolist()

    data_by_name[name] = data_for_name

print(data_by_name)

# Get the current date and time
current_date = datetime.now()

# Specify the path for the text file
text_file_path = f"Peer Review {current_date.date()}.txt"

# Write "hello" to the text file
if OUTPUT:
    with open(text_file_path, "w") as text_file:
        text_file.write("test\n")
