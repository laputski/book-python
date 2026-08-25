# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored, bm25_index, embed, reciprocal_rank_fusion, reranker, vector_store  # noqa: F401
# ─── листинг ───
from concurrent.futures import ThreadPoolExecutor

def search(query: str, k: int = 20) -> list[Scored]:
    vector = embed(query)
    with ThreadPoolExecutor(max_workers=2) as pool:
        f_dense = pool.submit(vector_store.search, vector, k)
        f_lex = pool.submit(bm25_index.search, query, k)
        dense, lexical = f_dense.result(), f_lex.result()
    fused = reciprocal_rank_fusion([dense, lexical])
    return reranker.rank(query, fused[:60])
