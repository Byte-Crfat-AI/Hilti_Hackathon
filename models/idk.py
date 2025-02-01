import requests
import json
import re

# Define the Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Model you want to use
MODEL_NAME = "deepseek-r1"

def clean_response(text):
    """Removes <think> and </think> tags from the response."""
    return re.sub(r"</?think>", "", text).strip()

def chat_with_ollama(prompt):
    """Sends a prompt to Ollama and cleans the response."""
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=data)

    if response.status_code == 200:
        result = response.json()
        cleaned_response = clean_response(result.get("response", ""))
        return cleaned_response
    else:
        return "Error: " + response.text

# Example Usage
user_prompt = "Hello!"
response = chat_with_ollama(user_prompt)
print("Ollama:", response)
