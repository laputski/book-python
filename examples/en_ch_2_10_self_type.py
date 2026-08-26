from dataclasses import dataclass, field, replace
from typing import Any, Self

@dataclass(frozen=True, slots=True)
class Query:
    text: str
    filters: dict[str, Any] = field(default_factory=dict)

    def with_filter(self, **fields: Any) -> Self:
        return replace(self, filters={**self.filters, **fields})

@dataclass(frozen=True, slots=True)
class GraphQuery(Query):
    depth: int = 1

    def with_depth(self, depth: int) -> Self:
        return replace(self, depth=depth)

GraphQuery("paths between entities").with_filter(kind="entity").with_depth(3)
