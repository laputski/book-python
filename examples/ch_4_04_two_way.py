# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Chunk  # noqa: F401
# ─── листинг ───
from collections.abc import Generator

def adaptive_batcher(initial: int = 64) -> Generator[tuple[Chunk, ...], Chunk | int | None, int]:
    """Отдаёт пакеты; принимает извне фрагмент либо новый размер пакета."""
    size, total = initial, 0
    buffer: list[Chunk] = []
    while True:
        chunk = yield tuple(buffer) if len(buffer) >= size else ()
        if isinstance(chunk, int):        # вызывающий сообщил новый размер
            size = max(1, chunk)
            continue
        if chunk is None:
            break
        buffer.append(chunk)
        if len(buffer) >= size:
            total += len(buffer)
            buffer.clear()
    return total
