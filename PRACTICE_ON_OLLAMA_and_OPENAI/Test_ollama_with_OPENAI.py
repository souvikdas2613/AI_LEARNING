from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
import os

messages = [{"role": "user", "content": "Who is IRON MAN ?"}]

MODEL_NAME = "qwen2.5:1.5b"

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

response = openai.chat.completions.create(
    model = MODEL_NAME, 
    messages = messages
)

print(response.choices[0].message.content)