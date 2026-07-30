import requests

payload = {
    "model": "llama3.2",
    "prompt": """
Open Services:
- 22/tcp SSH
- 80/tcp HTTP

Reply in less than 30 words.
""",
    "stream": False
}

response = requests.post(
    "http://localhost:11434/api/generate",
    json=payload,
    timeout=30
)

print(response.json()["response"])