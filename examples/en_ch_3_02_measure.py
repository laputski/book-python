import sys

def deep_size(obj: object, seen: set[int] | None = None) -> int:
    """The full size of an object together with what it references."""
    seen = set() if seen is None else seen
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_size(x, seen) for x in obj)
    else:
        slots = getattr(type(obj), "__slots__", ())
        for name in slots:
            if hasattr(obj, name):
                size += deep_size(getattr(obj, name), seen)
        d = getattr(obj, "__dict__", None)
        if d is not None:
            size += deep_size(d, seen)
    return size
