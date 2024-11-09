from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from os import environ


llm = ChatOpenAI(
    openai_api_key=environ.get('API_KEY'), 
    openai_api_base=environ.get('API_BASE'),
    model="gpt-4o"
)

template = """
We recorded conversations of a bunch of people with their best friends. Here are their transcriptions:

John: ....

Hamza: ....

William: ....

James: ....

Here is our transcription:
{transcription}

Based on our transcription, return the top 3 people that would seem most compatible for rooming. Base on the following guidelines:
- Tone of voice
- Personality
- Interests
- Liveliness
"""

prompt = template.format(transcription='blah blah')

response = llm.invoke(prompt)

print(response.content)