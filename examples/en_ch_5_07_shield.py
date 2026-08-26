# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Transaction  # noqa: F401
# ─── листинг ───
import asyncio

async def commit_safely(tx: Transaction) -> None:
    # Cancellation mid-commit would leave the transaction in limbo.
    await asyncio.shield(tx.commit())
