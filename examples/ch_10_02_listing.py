import math

def cosine_top_k(query: list[float], index: list[list[float]], k: int) -> list[int]:
    scores = []
    for i, row in enumerate(index):
        dot = sum(a * b for a, b in zip(query, row))
        norm = math.sqrt(sum(a * a for a in row))
        scores.append((dot / norm, i))
    scores.sort(reverse=True)
    return [i for _, i in scores[:k]]
