import heapq

import networkx as nx

def related(graph: nx.Graph, seeds: dict[str, float], top: int = 40) -> list[str]:
    scores = nx.pagerank(graph, alpha=0.85, personalization=seeds)
    for seed in seeds:
        scores.pop(seed, None)          # сами точки входа в выдачу не включаем
    return heapq.nlargest(top, scores, key=lambda node: scores[node])
