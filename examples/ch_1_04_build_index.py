from concurrent.futures import InterpreterPoolExecutor
from collections.abc import Iterable

def segment_shard(paths: list[str]) -> list[dict]:
    """Исполняется в отдельном интерпретаторе со своей блокировкой."""
    from corpus.segmentation import segment_file   # импорт внутри функции
    out: list[dict] = []
    for path in paths:
        out.extend(chunk.as_dict() for chunk in segment_file(path))
    return out

def build(shards: Iterable[list[str]], workers: int = 8) -> list[dict]:
    chunks: list[dict] = []
    with InterpreterPoolExecutor(max_workers=workers) as pool:
        for part in pool.map(segment_shard, shards):
            chunks.extend(part)
    return chunks
