from pathlib import Path

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"


def create_embedding(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def embed_chunks(chunks):
    embedded_chunks = []
    for chunk in chunks:
        embedding = create_embedding(chunk["text"])
        embedded_chunks.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "embedding": embedding,
        })
    return embedded_chunks