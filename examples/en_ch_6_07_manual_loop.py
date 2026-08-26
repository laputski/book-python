# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import main  # noqa: F401
# ─── листинг ───
import asyncio

loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())   # otherwise generators hang
    loop.run_until_complete(loop.shutdown_default_executor())
    loop.close()
