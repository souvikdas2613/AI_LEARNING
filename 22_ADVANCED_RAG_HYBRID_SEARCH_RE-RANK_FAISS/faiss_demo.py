import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = "text-embedding-3-small"

DOCS = [
    "Python is a high-level programming language.",
    "Kubernetes orchestrates containers in a cluster.",
    "FAISS finds nearest neighbor vectors very quickly.",
    "RAG retrieves documents then an LLM writes the answer.",
]


def create_embedding(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def demo_toy_vectors():
    """3-D vectors only — see how index.add / index.search work (no API)."""
    print("\n--- Part 1: toy vectors (IndexFlatL2, 3 dimensions) ---")
    vectors = np.array(
        [
            [0.1, 0.2, 0.3],
            [0.9, 0.8, 0.7],
            [0.2, 0.3, 0.4],
        ],
        dtype="float32",
    )
    index = faiss.IndexFlatL2(3)
    print (index)
    index.add(vectors)
    print (index)
    query = np.array([[0.1, 0.2, 0.3]], dtype="float32")
    distances, indices = index.search(query, k=2)
    print("query matches rows:", indices[0], "| L2 distances:", distances[0])


def demo_openai_faiss():
    """Embed each DOCS line, store in FAISS, search with a question vector."""
    if not os.getenv("OPENAI_API_KEY"):
        print("\n--- Part 2 skipped: set OPENAI_API_KEY in .env ---")
        return
    print("\n--- Part 2: OpenAI embeddings + FAISS (text-embedding-3-small) ---")
    vectors = np.array([create_embedding(text) for text in DOCS], dtype="float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    user_query = "How does fast vector search work in RAG?"
    query_vec = np.array([create_embedding(user_query)], dtype="float32")
    distances, indices = index.search(query_vec, k=2)
    print(f"Question: {user_query}\n")
    for rank, row in enumerate(indices[0], start=1):
        print(f"  {rank}. [{distances[0][rank - 1]:.4f}] {DOCS[row]}")


def main():
    demo_toy_vectors()
    demo_openai_faiss()


if __name__ == "__main__":
    main()