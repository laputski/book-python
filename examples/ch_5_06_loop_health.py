# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import log, serve  # noqa: F401
# --- the listing ---
import asyncio, time

async def monitor_lag(period: float = 0.5, threshold: float = 0.05) -> None:
    """Измеряет опоздание цикла: насколько сон длиннее заказанного."""
    while True:
        started = time.perf_counter()
        await asyncio.sleep(period)
        lag = time.perf_counter() - started - period
        if lag > threshold:
            log.warning("цикл событий опоздал на %.0f мс", lag * 1000)

async def main() -> None:
    loop = asyncio.get_running_loop()
    loop.slow_callback_duration = 0.05        # порог предупреждений в отладке
    async with asyncio.TaskGroup() as group:
        group.create_task(monitor_lag())
        group.create_task(serve())
