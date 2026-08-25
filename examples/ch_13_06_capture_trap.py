# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import kind, module  # noqa: F401
# ─── листинг ───
SIMPLE = "simple"

match kind:
    case SIMPLE:        # НЕ сравнение с SIMPLE: это захват в новое имя
        ...             # ветвь срабатывает всегда

match kind:
    case module.SIMPLE:  # сравнение: точка делает имя значением
        ...
    case "simple":       # сравнение: строка есть значение
        ...
