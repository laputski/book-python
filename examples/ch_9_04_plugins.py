# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Tool  # noqa: F401
# --- the listing ---
from importlib.metadata import entry_points

def load_plugins(group: str = "rag.tools") -> None:
    for point in entry_points(group=group):
        loaded = point.load()          # импорт происходит здесь и только здесь
        if not (isinstance(loaded, type) and issubclass(loaded, Tool)):
            raise TypeError(f"точка входа {point.name} не является инструментом")
