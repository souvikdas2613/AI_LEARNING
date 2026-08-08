# imports

import os
from dotenv import load_dotenv
import tiktoken

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


encoding = tiktoken.encoding_for_model(MODEL_NAME)

print ("\n\n\n===========EXAMPLE - 1 ===================================\n\n\n")

tokens = encoding.encode("Hi my name is Souvik")

print ("tokens")
print (tokens)

for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")


print ("\n\n\n===========EXAMPLE - 2 ===================================\n\n\n")

tokens = encoding.encode("Hi my name is Souvik and I have an umbrella")

print ("tokens")
print (tokens)

for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")