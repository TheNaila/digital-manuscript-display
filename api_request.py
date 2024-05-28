import requests

response = requests.get("http://127.0.0.1:5000/images", json = {"query": "china", "college": "ac"})

print(response.text)