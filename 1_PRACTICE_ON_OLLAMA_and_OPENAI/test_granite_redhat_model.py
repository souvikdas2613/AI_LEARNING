from dotenv import load_dotenv
load_dotenv(override=True)

import os

granite_api_key = os.getenv("REDHAT_GRANITE_API_KEY")
granite_base_url = os.getenv("REDHAT_GRANITE_BASE_URL")
granite_model = os.getenv("REDHAT_GRANITE_MODEL")

if granite_api_key:
    print("Red Hat Granite API Key is set")
else:
    print("Red Hat Granite API Key not set")


from openai import OpenAI

# Create an OpenAI-compatible client for the Red Hat Granite endpoint
granite = OpenAI(
    api_key=granite_api_key,
    base_url=granite_base_url
)

messages = [
    {
        "role": "user",
        "content": "Who is IRON MAN ?"
    }
]

# Call the Granite model
response = granite.chat.completions.create(
    model=granite_model,
    messages=messages
)

print(response.choices[0].message.content)
