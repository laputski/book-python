# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Chunk, Node, Tree, cluster, embed_batch, summarize  # noqa: F401
# --- the listing ---
from collections.abc import Iterator

import numpy as np

def build_tree(chunks: Iterator[tuple[Chunk, ...]], max_levels: int = 4) -> Tree:
    # Ленивая часть заканчивается здесь: уровень материализуется целиком.
    level: list[Node] = []
    vectors: list[np.ndarray] = []
    for batch in chunks:
        level.extend(Node.leaf(c) for c in batch)
        vectors.append(embed_batch([c.embedding_input for c in batch]))

    matrix = np.vstack(vectors)
    tree = Tree(leaves=level)
    for _ in range(max_levels):
        if len(level) <= 8:
            break
        groups = cluster(matrix, target_size=8)
        level = [Node.summary(summarize([level[i] for i in g])) for g in groups]
        matrix = embed_batch([n.text for n in level])
        tree.add_level(level)
    return tree
