from typing import Any


from pathlib import Path

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

    print(f"Loaded {len(docs)} documents")
    for doc in docs:
        print(f"  - {doc['doc_id']}")
        print(f"  - {doc['source']}")
    return docs


def preview(text, length=100):
    one_line = " ".join(text.split())
    if len(one_line) <= length:
        return one_line
    return one_line[: length - 3] + "..."


def keyword_score(query, text):
    query_words = set[Any](query.lower().split())
    text_words = set(text.lower().split())
    if not query_words:
        return 0.0
    matches = query_words & text_words
    return len(matches) / len(query_words)


def keyword_search(query, docs, top_k=2):
    results = []
    for doc in docs:
        print(f"Doc: {doc['source']}")
        score = keyword_score(query, doc["text"])
        results.append({
            "doc_id": doc["doc_id"],
            "source": doc["source"],
            "text": doc["text"],
            "keyword_score": score,
        })
    results.sort(key=lambda item: item["keyword_score"], reverse=True)
    print(f"\nResults: \n")
    for result in results:
        print(f"  - {result['source']}")
        print(f"    - {result['text']}")
        print(f"    - {result['keyword_score']}")   
        print("\n\n")
    return results[:top_k]


def main():
    docs = load_documents()
    if not docs:
        raise SystemExit(f"No .txt files in {DOCUMENTS_DIR}")
    print(f"Keyword search — {len(docs)} whole files (no chunking).")

    for query in DEMO_QUERIES:
        print(f"\nQuery: {query}")
        hits = keyword_search(query, docs, top_k=3)
        for rank, hit in enumerate(hits, start=1):
            print(
                f"  {rank}. score={hit['keyword_score']:.4f} "
                f"{hit['source']}: {preview(hit['text'])}"
            )


if __name__ == "__main__":
    main()