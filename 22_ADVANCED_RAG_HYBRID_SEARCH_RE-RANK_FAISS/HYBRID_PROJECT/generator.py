from pathlib import Path

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL")


def generate_answer(query, results):
    context = "\n\n".join(result["text"] for result in results)
    prompt = f"""
Answer the user's question using only the provided context.

Context:
{context}

Question:
{query}

Rules:
1. Use only the provided context.
2. Do not invent information.
3. If the answer is not present, say that the information is not available.
4. Give a clear and concise answer.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()