from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
import os

messages = [{"role": "user", "content": "Who is IRON MAN ?"}]

MODEL_NAME = "gpt-4.1-nano"

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print("We have OPENAI KEY Loaded")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")

openai = OpenAI()

response = openai.chat.completions.create(
    model = MODEL_NAME,
    messages = messages
)

print(response.choices[0].message.content)
