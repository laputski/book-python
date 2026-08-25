# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import normalize, read_text  # noqa: F401
# ─── листинг ───
import json
from collections.abc import Iterator
from pathlib import Path

def resumable(paths: list[str], cursor: Path) -> Iterator[tuple[str, str]]:
    """Проход по корпусу, переживающий перезапуск."""
    done: set[str] = set()
    if cursor.exists():
        done = set(json.loads(cursor.read_text(encoding="utf-8")))
    processed = list(done)
    for path in paths:
        if path in done:
            continue
        yield path, normalize(read_text(path))
        processed.append(path)
        if len(processed) % 500 == 0:                # запись не на каждом шаге
            cursor.write_text(json.dumps(processed, ensure_ascii=False),
                              encoding="utf-8")
    cursor.write_text(json.dumps(processed, ensure_ascii=False), encoding="utf-8")
