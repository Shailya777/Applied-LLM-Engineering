import requests

# Ping the exact localhost port where WSL Ollama is broadcasting:
url = "http://172.23.37.63:11434/api/generate"

# Ask our specific Llama model a quick question:
payload = {
    "model": "llama3.1:8b",
    "prompt": "Hi, Shailya here. Talking to you from Pycharm Editor. I ams starting to learn GenAI for my Data Science / Data Analytics Tech Stack. Reply like you are Mike Ehrmantraut from Breaking Bad. ",
    "stream": False
}

# Sending The Request and Print The AI's Response:
response = requests.post(url, json=payload)
print(response.json()['response'])