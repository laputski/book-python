# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import main  # noqa: F401
# --- the listing ---
import asyncio

loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())   # otherwise generators hang
    loop.run_until_complete(loop.shutdown_default_executor())
    loop.close()
