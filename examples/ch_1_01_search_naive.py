# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored, bm25_index, embed, reciprocal_rank_fusion, reranker, vector_store  # noqa: F401
# ─── листинг ───
def search(query: str, k: int = 20) -> list[Scored]:
    vector = embed(query)                      # ≈ 30 мс, обращение к службе
    dense = vector_store.search(vector, k)     # ≈ 120 мс, обращение к хранилищу
    lexical = bm25_index.search(query, k)      # ≈ 40 мс, обращение к индексу
    fused = reciprocal_rank_fusion([dense, lexical])
    return reranker.rank(query, fused[:60])    # ≈ 200 мс, обращение к службе
