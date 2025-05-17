import requests
import json

headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

data = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [
        {"role": "user", "content": "hello"}
    ]
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps(data),
)

# print(response.json()["choices"][0]["message"]["content"])
print(response.json())



