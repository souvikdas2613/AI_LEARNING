import os
from pathlib import Path

from dotenv import load_dotenv

from advanced_rag import build_rag, retrieve
from generator import generate_answer

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv()

DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set — add it to .env")
    if not os.getenv("OPENAI_MODEL"):
        raise SystemExit("OPENAI_MODEL not set — add it to .env")
    paths = sorted(DOCUMENTS_DIR.glob("*.txt"))
    if not paths:
        raise SystemExit(f"No .txt files in {DOCUMENTS_DIR}")
    print("Building RAG knowledge base (whole files, chunking off for now)...")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        build_rag(text, path.name, chunk=False)
        print(f"  indexed {path.name}")
    print("\nAdvanced RAG is ready.")
    while True:
        query = input("\nYou : ").strip()
        if query.lower() in {"exit", "quit"}:
            break
        results = retrieve(query, top_k=5)
        print("\nRetrieved Sources Ranking:")
        for result in results:
            print(f"- {result['source']} (chunk {result['chunk_id']})")
        answer = generate_answer(query, results)
        print("\nRAG :")
        print(answer)


if __name__ == "__main__":
    main()