# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored, classify, generate, grounded, question, retrieve, rewrite  # noqa: F401
# --- the listing ---
from typing import Any


async def _excerpt() -> Any:
    need_retrieval = classify(question) != "simple"
    done, steps, draft = False, 0, ""
    context: list[Scored] = []
    while not done:
        if need_retrieval and not context:
            context = await retrieve(question)
        draft = await generate(question, context)
        if need_retrieval and not grounded(draft, context):
            question = rewrite(question, draft)
            context = []
            steps += 1
            if steps > 3:
                done = True
        else:
            done = True
