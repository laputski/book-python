import importlib
from typing import Any

_LAZY = {"GraphTool": ".graph", "SqlTool": ".sql", "VisionTool": ".vision"}

def __getattr__(name: str) -> Any:          # PEP 562: module attribute access
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"module {__name__} has no attribute {name!r}")
    return getattr(importlib.import_module(module, __name__), name)

def __dir__() -> list[str]:
    return sorted(_LAZY)
