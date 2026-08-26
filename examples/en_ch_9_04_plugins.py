# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Tool  # noqa: F401
# ─── листинг ───
from importlib.metadata import entry_points

def load_plugins(group: str = "rag.tools") -> None:
    for point in entry_points(group=group):
        loaded = point.load()          # the import happens here and only here
        if not (isinstance(loaded, type) and issubclass(loaded, Tool)):
            raise TypeError(f"entry point {point.name} is not a tool")
