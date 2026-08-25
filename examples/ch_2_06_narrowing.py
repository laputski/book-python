# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import GraphHit, Scored  # noqa: F401
# ─── листинг ───
from typing import TypeIs

def is_graph_hit(hit: Scored) -> TypeIs[GraphHit]:
    return hit.kind == "node_edge"

def explain(hit: Scored) -> str:
    if is_graph_hit(hit):
        return f"путь длиной {len(hit.path)}"   # hit сужен до GraphHit
    return hit.chunk.text[:200]
