def keyword_score(query, text):
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    if not query_words:
        return 0.0
    matches = query_words & text_words
    return len(matches) / len(query_words)
