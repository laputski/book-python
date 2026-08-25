def collect(graph, seeds: list[str], depth: int = 3) -> set[str]:
    seen, frontier = set(seeds), set(seeds)
    for _ in range(depth):
        frontier = {n for node in frontier for n in graph.neighbors(node)} - seen
        seen |= frontier
    return seen
