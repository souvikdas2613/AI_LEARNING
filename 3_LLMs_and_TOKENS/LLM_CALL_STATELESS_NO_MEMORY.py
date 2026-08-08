# imports

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
else:
    print("API key found and looks good so far!")

if not MODEL_NAME:
    print("\n\nNo model name was found - please head over to the .env file to identify & fix!")
else:
    print("\n\nModel name found " + MODEL_NAME + " and looks good so far!\n\n")


openai = OpenAI()

print ("\n\n\n===========CALL LLM - STATELESS - NO MEMORY ===================================\n\n\n")

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Souvik"}
    ]

response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
reply_1 = response.choices[0].message.content
print(reply_1)


print ("\n\n\n===========CALL LLM - STATELESS - NO MEMORY - 2 ===================================\n\n\n")

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
    ]

response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
print(response.choices[0].message.content)


print ("\n\n\n===========CALL LLM - WITH FULL HISTORY (FAKE MEMORY) - 3 ===================================\n\n\n")

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Souvik"},
    {"role": "assistant", "content": reply_1},
    {"role": "user", "content": "What's my name?"}
    ]

response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
print(response.choices[0].message.content)
