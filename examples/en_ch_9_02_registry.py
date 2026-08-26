# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import render, search  # noqa: F401
# ─── листинг ───
from typing import Any, ClassVar

class Tool:
    """The base of the tool family. A subclass enters the registry upon declaration."""

    registry: ClassVar[dict[str, type["Tool"]]] = {}
    name: ClassVar[str]
    description: ClassVar[str]

    def __init_subclass__(cls, /, abstract: bool = False, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if abstract:
            return
        if not getattr(cls, "name", None):
            raise TypeError(f"{cls.__qualname__} declared no tool name")
        if cls.name in Tool.registry:
            other = Tool.registry[cls.name].__qualname__
            raise TypeError(f"the name {cls.name!r} is already taken by {other}")
        Tool.registry[cls.name] = cls

    async def run(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError            # a subclass declares its own arguments

class SearchTool(Tool):
    name = "search"
    description = "Find corpus chunks for a natural-language query."

    async def run(self, query: str, k: int = 8) -> str:
        return render(await search(query, k))
