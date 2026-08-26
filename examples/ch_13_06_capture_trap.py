# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import kind, module  # noqa: F401
# --- the listing ---
SIMPLE = "simple"

match kind:
    case SIMPLE:        # НЕ сравнение с SIMPLE: это захват в новое имя
        ...             # ветвь срабатывает всегда

match kind:
    case module.SIMPLE:  # сравнение: точка делает имя значением
        ...
    case "simple":       # сравнение: строка есть значение
        ...
