import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# First API call without reasoning
try:
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    },
    json={
        "model": os.getenv("OPENROUTER_MODEL"),
        "messages": [
            {
                "role": "user",
                "content": "Write me a python function that checks for prime numbers"
            },
        ],
    },
    timeout=60,
)

  data = response.json()
  output = data["choices"][0]["message"]["content"]
  print(output)
  # print(json.dumps(data, indent=2))

# except requests.exceptions.Timeout:
#     print("Request timed out. The model/provider took too long to respond.")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")