# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Transaction  # noqa: F401
# --- the listing ---
import asyncio

async def commit_safely(tx: Transaction) -> None:
    # Отмена во время подтверждения оставила бы транзакцию в неопределённом виде.
    await asyncio.shield(tx.commit())
