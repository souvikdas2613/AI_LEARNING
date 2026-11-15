import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = "text-embedding-3-small"

DOCUMENTS_DIR = Path(__file__).resolve().parents[1] / "documents"

DEMO_QUERIES = [
    "How do I list pods with kubectl?",
    "How do I define a function in Python?",
    "What is RAII in C++?",
]


def load_documents():
    docs = []
    for doc_id, path in enumerate(sorted(DOCUMENTS_DIR.glob("*.txt"))):
        docs.append({
            "doc_id": doc_id,
            "source": path.name,
            "text": path.read_text(encoding="utf-8"),
        })
    return docs


def preview(text, length=100):
    one_line = " ".join(text.split())
    if len(one_line) <= length:
        return one_line
    return one_line[: length - 3] + "..."


def create_embedding(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def build_index(docs):
    indexed = []
    for doc in docs:
        embedding = create_embedding(doc["text"])
        record = {
            "doc_id": doc["doc_id"],
            "source": doc["source"],
            "text": doc["text"],
            "embedding": embedding,
        }
        indexed.append(record)
        print(f"Indexed:\n {doc['source']}")
        print(f"  - {doc['doc_id']}")
        print(f"  - {doc['source']}")
        print(f"  - embedding dim: {len(embedding)}")
        print(f"  - {doc['text']}")
        print("\n\n")
    return indexed


def semantic_search(query, index, top_k=3):
    query_embedding = create_embedding(query)
    print(f"Query embedding dim: {len(query_embedding)}")
    results = []
    for row in index:
        score = cosine_similarity(query_embedding, row["embedding"])
        results.append({
            "doc_id": row["doc_id"],
            "source": row["source"],
            "text": row["text"],
            "semantic_score": score,
        })
    results.sort(key=lambda item: item["semantic_score"], reverse=True)
    print(f"\nResults: \n")
    for result in results:
        print(f"  - {result['source']}")
        print(f"    - {result['text']}")
        print(f"    - {result['semantic_score']}")   
        print("\n\n")   
    return results[:top_k]


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set — add it to .env")
    
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    if not docs:
        raise SystemExit(f"No .txt files in {DOCUMENTS_DIR}")

    print(f"Semantic search — embedding {len(docs)} whole files (no chunking).")
    
    for doc in docs:
        print(f"  - {doc['source']}")
    
    print("\nBuilding index...")
    
    index = build_index(docs)
    
    print(f"Index built with {len(index)} documents")
    print("BEGINNING SEARCH...\n")
    for query in DEMO_QUERIES:
        print(f"\nQuery: {query}")
        hits = semantic_search(query, index, top_k=3)
        for rank, hit in enumerate(hits, start=1):
            print(
                f"  {rank}. score={hit['semantic_score']:.4f} "
                f"{hit['source']}: {preview(hit['text'])}"
            )


if __name__ == "__main__":
    main()