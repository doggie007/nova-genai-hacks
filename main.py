from dotenv import load_dotenv
load_dotenv()

from os import environ
import requests
import json

TEAM_API_KEY = environ.get('TEAM_API_KEY')
PROXY_ENDPOINT = environ.get('PROXY_ENDPOINT')
CARTESIA_KEY = environ.get('CARTESIA_KEY')

# path_of_voice: mp3 file of the voice to clone
# returns voice embedding (vector)
def clone_voice(path_of_voice):
    url = "https://api.cartesia.ai/voices/clone/clip"
    headers = {
        "X-API-Key": CARTESIA_KEY, 
        "Cartesia-Version": "2024-06-10",
    }

    files = {
        'clip': (path_of_voice, open(path_of_voice, 'rb'), 'audio/mpeg'),
    }
    data = {
        'enhance': 'true'
    }
    response = requests.post(url, headers=headers, files=files, data=data)

    return response.json()['embedding']

# embedding: embedding of the voice
# transcript: the thing you want to say
# returns: the binary of the wav file
def speak(embedding, transcript):
    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "X-API-Key": CARTESIA_KEY,
        "Cartesia-Version": "2024-06-10",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "sonic-english",
        "transcript": transcript,
        "voice": {
            "mode": "embedding",
            "embedding": embedding
        },
        "output_format": {
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100
            },
        "language": "en"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.content