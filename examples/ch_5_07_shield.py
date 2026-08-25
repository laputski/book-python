# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Transaction  # noqa: F401
# ─── листинг ───
import asyncio

async def commit_safely(tx: Transaction) -> None:
    # Отмена во время подтверждения оставила бы транзакцию в неопределённом виде.
    await asyncio.shield(tx.commit())
