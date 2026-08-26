# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DECAY, Graph, Node  # noqa: F401
# --- the listing ---
import heapq
from collections.abc import Iterator

def budgeted_walk(graph: Graph, seeds: dict[str, float], *,
                  width: int = 8, depth: int = 4,
                  token_budget: int = 6000) -> Iterator[Node]:
    """A walk bounded in width, depth, and gathered volume."""
    heap: list[tuple[float, int, str]] = [(-w, 0, n) for n, w in seeds.items()]
    heapq.heapify(heap)
    visited: set[str] = set()
    spent = 0

    while heap and spent < token_budget:
        weight, level, node_id = heapq.heappop(heap)
        if node_id in visited:
            continue
        visited.add(node_id)
        node = graph.node(node_id)
        spent += node.token_cost
        yield node
        if level >= depth:
            continue
        neighbours = graph.rank_neighbours(node_id, limit=width)
        for neighbour, edge_weight in neighbours:
            if neighbour not in visited:
                # weight is stored negated for the min-heap
                decayed = -weight * edge_weight * DECAY
                heapq.heappush(heap, (-decayed, level + 1, neighbour))
