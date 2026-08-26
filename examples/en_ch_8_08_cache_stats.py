from dataclasses import dataclass

@dataclass(slots=True)
class CacheStats:
    hits: int = 0
    misses: int = 0
    joined: int = 0        # awaited someone else's computation instead of starting one
    evicted: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    @property
    def coalescing_rate(self) -> float:
        """The share of misses removed by joining simultaneous requests."""
        return self.joined / self.misses if self.misses else 0.0
