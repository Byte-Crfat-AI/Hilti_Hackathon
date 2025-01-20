import requests

def get_intent(query):
    url = 'http://localhost:5005/model/parse'
    data = {
        "text": query
    }
    response = requests.post(url, json=data)
    intent = response.json()['intent']['name']
    return intent

# Example
# query = "Give a brief description about Artificial Intelligence"
# print(get_intent(query))
