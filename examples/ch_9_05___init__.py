import importlib
from typing import Any

_LAZY = {"GraphTool": ".graph", "SqlTool": ".sql", "VisionTool": ".vision"}

def __getattr__(name: str) -> Any:          # <a class="pep" href="https://peps.python.org/pep-0562/" target="_blank" rel="noreferrer">PEP 562</a>: обращение к атрибуту модуля
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"модуль {__name__} не содержит {name!r}")
    return getattr(importlib.import_module(module, __name__), name)

def __dir__() -> list[str]:
    return sorted(_LAZY)
