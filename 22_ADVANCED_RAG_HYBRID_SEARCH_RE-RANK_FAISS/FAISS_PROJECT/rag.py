from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
import faiss
from pathlib import Path

# Same .env habit as other chapter demos (AI_LEARNING root + cwd)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Embedding model ≠ chat model

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.getenv("MODEL_NAME")
client = OpenAI()

# How many nearest docs FAISS should return (1 = same as naive “best doc”)
TOP_K = 1


def load_documents():
    documents = {}
    folder = Path(__file__).resolve().parent / "knowledge"
    for file in folder.glob("*.txt"):
        documents[file.name] = file.read_text(
            encoding="utf-8"
        )
    return documents


def create_embedding(content):
    embedding1 = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=content,
    ).data[0].embedding
    return embedding1


documents = load_documents()

# Stable row order so FAISS index i ↔ filenames[i] ↔ documents[name]
filenames = list(documents.keys())
vectors = np.array(
    [create_embedding(documents[name]) for name in filenames],
    dtype="float32",
)

# --- FAISS in the middle (replaces the cosine loop in naive rag.py) ---
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)
print(f"\n\nFAISS index ready: {index.ntotal} vectors, dim={vectors.shape[1]}")

print("\n\n" + "=" * 40)
print("      My AI Assistant (FAISS)")
print("=" * 40 + "\n")

while True:
    user_input = input("\nYou : ")
    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    question_embedding = create_embedding(user_input)
    query = np.array([question_embedding], dtype="float32")
    distances, indices = index.search(query, k=TOP_K)

    for rank, row in enumerate(indices[0]):
        print(f"Rank {rank + 1}: {filenames[row]}  (L2 distance: {distances[0][rank]:.4f})")

    best_document = filenames[indices[0][0]]
    print(f"Best document: {best_document}")

    RAG_DOC_CONTENT = documents[best_document]
    print(f"\nRAG_DOC_CONTENT: {RAG_DOC_CONTENT}")

    prompt = f"Use ONLY the Context below to answer.\nIf the user typed a topic or keyword (not a full question), briefly explain what it is using the Context.\nIf the Context truly has nothing relevant, say 'I don't know.'\n\nRAG_Context: {RAG_DOC_CONTENT}\n\nUSER_INPUT: {user_input}"

    print(f"\n\nAI_ASSISTANT_PROMPT: {prompt}")

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    print("\nAI :", response.choices[0].message.content)
