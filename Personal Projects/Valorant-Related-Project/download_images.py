from PIL import Image
import requests
from io import BytesIO

response = requests.get("https://valorant-api.com/v1/agents")
data = response.json()
main_data = data["data"]

training_data = {}
for agent in main_data:
    abilities = agent.get("abilities")
    roles = agent.get("role")

    for item in abilities:
        if roles is not None:
            training_data[item.get("displayIcon")] = roles.get("displayName")

counter = 0
for key, value in training_data.items():
    if key is None:
        continue
    response_image = requests.get(key)
    img = Image.open(BytesIO(response_image.content))
    resized_img = img.resize((128, 128))
    resized_img.save(fp=f"{value}_{counter}.png")
    counter += 1
