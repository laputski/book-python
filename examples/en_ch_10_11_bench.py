import time
from collections.abc import Callable
from statistics import median

def bench(fn: Callable[[], object], *, warmup: int = 3, runs: int = 15) -> float:
    """The median time in milliseconds; the median resists outliers better than the mean."""
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(runs):
        started = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - started) * 1000)
    return median(samples)
