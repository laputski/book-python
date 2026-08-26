# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import kind, module  # noqa: F401
# ─── листинг ───
SIMPLE = "simple"

match kind:
    case SIMPLE:        # NOT a comparison with SIMPLE: a capture into a new name
        ...             # this branch always fires

match kind:
    case module.SIMPLE:  # a comparison: the dot makes the name a value
        ...
    case "simple":       # a comparison: a literal is a value
        ...
