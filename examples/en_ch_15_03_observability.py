# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import request_id  # noqa: F401
# ─── листинг ───
import logging, time
from contextlib import contextmanager

log = logging.getLogger("rag")

@contextmanager
def stage(name: str, **fields: object):
    started = time.perf_counter()
    try:
        yield
    finally:
        log.info("stage", extra={
            "stage": name,
            "duration_ms": round((time.perf_counter() - started) * 1000, 1),
            "request_id": request_id.get(),     # the context variable of Chapter 7
            **fields,
        })
