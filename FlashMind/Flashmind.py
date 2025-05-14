import requests
import json

headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

data = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [
        {"role": "user", "content": "Write a bedtime story about a flying squirrel."}
    ]
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps(data),
)

# print(response.json()["choices"][0]["message"]["content"])
print(response.json())



