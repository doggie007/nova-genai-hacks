from dotenv import load_dotenv
load_dotenv()

from os import environ
import requests
import json

TEAM_API_KEY = environ.get('TEAM_API_KEY')
PROXY_ENDPOINT = environ.get('PROXY_ENDPOINT')
CARTESIA_KEY = environ.get('CARTESIA_KEY')

url = "https://api.cartesia.ai/voices/clone/clip"
headers = {
    "X-API-Key": CARTESIA_KEY, 
    "Cartesia-Version": "2024-06-10",
}

files = {
    'clip': ('jose.mp3', open('jose.mp3', 'rb'), 'audio/mpeg'),
}
data = {
    'enhance': 'true'
}
response = requests.post(url, headers=headers, files=files, data=data)

print(response.status_code)
print(response.json())