# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Tool, json_schema_for  # noqa: F401
# --- the listing ---
import inspect, typing

def describe(tool: type[Tool]) -> dict[str, object]:
    signature = inspect.signature(tool.run)
    hints = typing.get_type_hints(tool.run)
    properties: dict[str, object] = {}
    required: list[str] = []
    for name, parameter in signature.parameters.items():
        if name in ("self", "kwargs"):
            continue
        properties[name] = json_schema_for(hints.get(name, str))
        if parameter.default is inspect.Parameter.empty:
            required.append(name)
    return {
        "name": tool.name,
        "description": inspect.cleandoc(tool.description),
        "parameters": {"type": "object", "properties": properties, "required": required},
    }
