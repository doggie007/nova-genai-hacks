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

vector = response.json()['embedding']
transcript = 'I love Hamza, I love James, I love William'

response = requests.post(
  "https://api.cartesia.ai/tts/bytes",
  headers={
    "X-API-Key": CARTESIA_KEY,
    "Cartesia-Version": "2024-06-10",
    "Content-Type": "application/json"
  },
  json={
    "model_id": "sonic-english",
    "transcript": transcript,
    "voice": {
      "mode": "embedding",
      "embedding": vector
    },
    "output_format": {
      "container": "mp3",
      "bit_rate": 128000,
      "sample_rate": 44100
    },
    "language": "en"
  },
)

print(response)