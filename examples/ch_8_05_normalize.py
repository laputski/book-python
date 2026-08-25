# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import DenseHit, LexicalHit, Scored  # noqa: F401
# ─── листинг ───
from functools import singledispatch

@singledispatch
def normalize(hit: Scored) -> float:
    raise NotImplementedError(f"нет правила для {type(hit).__name__}")

@normalize.register
def _(hit: DenseHit) -> float:
    return (hit.score + 1.0) / 2.0            # из отрезка [-1, 1] в [0, 1]

@normalize.register
def _(hit: LexicalHit) -> float:
    return hit.score / (hit.score + 1.0)      # сжатие неограниченной шкалы
