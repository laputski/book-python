# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Transaction  # noqa: F401
# --- the listing ---
import asyncio

async def commit_safely(tx: Transaction) -> None:
    # Cancellation mid-commit would leave the transaction in limbo.
    await asyncio.shield(tx.commit())
