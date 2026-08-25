# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import render, search  # noqa: F401
# ─── листинг ───
from typing import Any, ClassVar

class Tool:
    """Основа семейства инструментов. Подкласс попадает в реестр при объявлении."""

    registry: ClassVar[dict[str, type["Tool"]]] = {}
    name: ClassVar[str]
    description: ClassVar[str]

    def __init_subclass__(cls, /, abstract: bool = False, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if abstract:
            return
        if not getattr(cls, "name", None):
            raise TypeError(f"{cls.__qualname__} не объявил имя инструмента")
        if cls.name in Tool.registry:
            other = Tool.registry[cls.name].__qualname__
            raise TypeError(f"имя {cls.name!r} уже занято классом {other}")
        Tool.registry[cls.name] = cls

    async def run(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError            # подкласс объявляет свои аргументы

class SearchTool(Tool):
    name = "search"
    description = "Найти фрагменты корпуса по запросу на естественном языке."

    async def run(self, query: str, k: int = 8) -> str:
        return render(await search(query, k))
