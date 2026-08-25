def made_progress(previous: frozenset[str], current: frozenset[str],
                  threshold: float = 0.2) -> bool:
    """Продвижение есть, если извлечено заметно новое."""
    if not current:
        return False
    fresh = current - previous
    return len(fresh) / len(current) >= threshold
