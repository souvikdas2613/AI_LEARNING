from dotenv import load_dotenv
load_dotenv(override=True)

import os

enmaas_api_key = os.getenv("REDHAT_ENMAAS_API_KEY")
enmaas_base_url = os.getenv("REDHAT_ENMAAS_BASE_URL")
enmaas_model = os.getenv("REDHAT_ENMAAS_MODEL")

if enmaas_api_key:
    print("Red Hat ENMAAS API Key is set")
else:
    print("Red Hat ENMAAS API Key not set")


from openai import OpenAI

# Create an OpenAI-compatible client for the Red Hat ENMAAS endpoint
enmaas = OpenAI(
    api_key=enmaas_api_key,
    base_url=enmaas_base_url
)

messages = [
    {
        "role": "user",
        "content": "Who is IRON MAN ?"
    }
]

# Call the ENMAAS model
response = enmaas.chat.completions.create(
    model=enmaas_model,
    messages=messages
)

print(response.choices[0].message.content)
