# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import log, serve  # noqa: F401
# ─── листинг ───
import asyncio, time

async def monitor_lag(period: float = 0.5, threshold: float = 0.05) -> None:
    """Measures the loop's lag: how much longer a sleep takes than requested."""
    while True:
        started = time.perf_counter()
        await asyncio.sleep(period)
        lag = time.perf_counter() - started - period
        if lag > threshold:
            log.warning("event loop lagged by %.0f ms", lag * 1000)

async def main() -> None:
    loop = asyncio.get_running_loop()
    loop.slow_callback_duration = 0.05        # warning threshold in debug mode
    async with asyncio.TaskGroup() as group:
        group.create_task(monitor_lag())
        group.create_task(serve())
