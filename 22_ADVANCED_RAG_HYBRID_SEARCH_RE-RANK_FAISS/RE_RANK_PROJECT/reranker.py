"""Cross-encoder re-rank: jointly score (query, document) pairs.

Uses a small local model — no extra LLM calls for scoring.
"""

from sentence_transformers import CrossEncoder

# Lightweight MS MARCO cross-encoder — common second-stage RAG reranker
MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = CrossEncoder(MODEL_NAME)
    return _model


def rerank(query, candidates, top_k=3):
    """Score each candidate with a cross-encoder; return top_k by relevance."""
    if not candidates:
        return []

    model = _get_model()

    # 1) Ask the model: how relevant is each doc to this query?
    pairs = []
    for candidate in candidates:
        pairs.append((query, candidate["text"]))
    scores = model.predict(pairs)
    print ("scores:")
    print(scores)

    # 2) Put the score on each candidate
    scored = []
    for i in range(len(candidates)):
        item = candidates[i].copy()
        item["rerank_score"] = float(scores[i])
        scored.append(item)

    # 3) Best score first, keep only top_k
    scored.sort(key=lambda item: item["rerank_score"], reverse=True)
    return scored[:top_k]

