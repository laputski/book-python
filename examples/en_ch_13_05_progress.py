def made_progress(previous: frozenset[str], current: frozenset[str],
                  threshold: float = 0.2) -> bool:
    """There is progress if the retrieval brought noticeably new material."""
    if not current:
        return False
    fresh = current - previous
    return len(fresh) / len(current) >= threshold
