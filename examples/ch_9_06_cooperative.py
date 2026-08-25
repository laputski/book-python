# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import wrap_public_methods  # noqa: F401
# ─── листинг ───
from typing import ClassVar

class Registered:
    registry: ClassVar[dict[str, type]] = {}

    def __init_subclass__(cls, /, name: str = "", **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)      # передаём остальное дальше
        if name:
            Registered.registry[name] = cls

class Traced:
    def __init_subclass__(cls, /, traced: bool = True, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if traced:
            wrap_public_methods(cls)

class SearchTool(Registered, Traced, name="search", traced=True):
    ...
