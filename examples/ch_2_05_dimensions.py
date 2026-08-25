# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Bm25Retriever, DenseRetriever, GraphRetriever, Retriever  # noqa: F401
# ─── листинг ───
from typing import Annotated, Literal, TypedDict

SearchOperator = Literal["ann", "lexical", "graph_traversal",
                         "boolean_query", "tree_navigation", "spatial_range"]
Fusion = Literal["none", "rrf", "score_normalization", "learned_fusion"]

Score = Annotated[float, "нормализованная оценка в отрезке от нуля до единицы"]

class SourceSpec(TypedDict):
    """Описание источника в конфигурации, приходящей из файла."""
    name: str
    operator: SearchOperator
    weight: float

def build_source(spec: SourceSpec) -> Retriever:
    match spec["operator"]:
        case "ann":
            return DenseRetriever(spec["name"])
        case "lexical":
            return Bm25Retriever(spec["name"])
        case "graph_traversal":
            return GraphRetriever(spec["name"])
        case _:
            raise NotImplementedError(spec["operator"])
