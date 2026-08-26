# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Bm25Retriever, DenseRetriever, GraphRetriever, Retriever  # noqa: F401
# --- the listing ---
from typing import Annotated, Literal, TypedDict

SearchOperator = Literal["ann", "lexical", "graph_traversal",
                         "boolean_query", "tree_navigation", "spatial_range"]
Fusion = Literal["none", "rrf", "score_normalization", "learned_fusion"]

Score = Annotated[float, "normalized score in the interval from zero to one"]

class SourceSpec(TypedDict):
    """A source's description in configuration arriving from a file."""
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
