# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import dataclass, field  # noqa: F401
# ─── листинг ───
@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    text: str = field(compare=False)      # не участвует ни в сравнении, ни в хеше
    context: str = field(compare=False, default="")
