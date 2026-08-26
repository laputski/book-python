# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored, bm25_index, embed, reciprocal_rank_fusion, reranker, vector_store  # noqa: F401
# ─── листинг ───
def search(query: str, k: int = 20) -> list[Scored]:
    vector = embed(query)                      # ≈ 30 ms, a call to a service
    dense = vector_store.search(vector, k)     # ≈ 120 ms, a call to the store
    lexical = bm25_index.search(query, k)      # ≈ 40 ms, a call to the index
    fused = reciprocal_rank_fusion([dense, lexical])
    return reranker.rank(query, fused[:60])    # ≈ 200 ms, a call to a service
