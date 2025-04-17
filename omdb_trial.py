import requests

API_KEY = "6d6267b5" # <--- Ersetze das mit deinem echten Key
title = "Titanic"

url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
response = requests.get(url)
data = response.json()

print(data)
