import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "Qwen/Qwen2.5-7B-Instruct:together"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model = MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message.content)
