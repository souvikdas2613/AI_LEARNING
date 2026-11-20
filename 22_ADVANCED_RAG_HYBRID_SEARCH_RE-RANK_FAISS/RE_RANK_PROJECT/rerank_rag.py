from chunker import create_chunks
from embeddings import embed_chunks, create_embedding
from chroma_store import add_chunks, search
from retriever import keyword_score
from reranker import rerank


def build_rag(text, source, chunk=False):
    if chunk:
        chunks = create_chunks(text, source=source, chunk_size=200, overlap=50)
    else:
        chunks = [{"text": text, "source": source, "chunk_id": 0}]
    embedded_chunks = embed_chunks(chunks)
    add_chunks(embedded_chunks)
    return embedded_chunks


def retrieve(query, top_k=5):
    """Hybrid shortlist, then LLM re-rank → top 3 for the prompt."""
    query_embedding = create_embedding(query)
    semantic_results = search(query_embedding, top_k=top_k)
    candidates = []
    documents = semantic_results["documents"][0]
    metadatas = semantic_results["metadatas"][0]
    distances = semantic_results["distances"][0]
    for i in range(len(documents)):
        text = documents[i]
        metadata = metadatas[i]
        distance = distances[i]
        semantic = 1 / (1 + distance)
        keyword = keyword_score(query, text)
        combined = 0.7 * semantic + 0.3 * keyword
        candidates.append({
            "text": text,
            "source": metadata["source"],
            "chunk_id": metadata["chunk_id"],
            "semantic_score": semantic,
            "keyword_score": keyword,
            "combined_score": combined,
        })
    candidates.sort(key=lambda item: item["combined_score"], reverse=True)
    candidates = candidates[:top_k]
    print("\n1) Hybrid shortlist (before re-rank):")
    for candidate in candidates:
        print(
            f"- {candidate['source']}  "
            f"semantic={candidate['semantic_score']:.3f}  "
            f"keyword={candidate['keyword_score']:.3f}  "
            f"combined={candidate['combined_score']:.3f}"
        )
    print(f"\n2) LLM re-rank → keep top 3 (scores 0–100)...")
    return rerank(query, candidates, top_k=3)
