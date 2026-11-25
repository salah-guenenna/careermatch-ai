from functools import lru_cache


@lru_cache(maxsize=1)
def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except ImportError:
        return None


def semantic_similarity(cv_text: str, job_text: str) -> float | None:
    """Return cosine similarity only when the optional model is installed."""
    model = _load_model()
    if model is None:
        return None
    embeddings = model.encode([cv_text, job_text], normalize_embeddings=True)
    return float(embeddings[0] @ embeddings[1])

