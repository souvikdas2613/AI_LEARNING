import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv(override=True)

client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message.content)

