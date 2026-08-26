# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import bm25_index, k, query, vector, vector_store  # noqa: F401
# ─── листинг ───
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=2) as pool:
    f_dense = pool.submit(vector_store.search, vector, k)
    f_lex = pool.submit(bm25_index.search, query, k)
    dense, lexical = f_dense.result(), f_lex.result()
