# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Cited, THRESHOLD, attach_citations, build_prompt, finish_without_lookahead, merge, model, retrieve, sentences_with_confidence, strip_uncertain_spans  # noqa: F401
# --- the listing ---
from collections.abc import AsyncIterator
from contextlib import aclosing

async def answer_with_lookahead(question: str, budget: int = 4) -> AsyncIterator[Cited]:
    context = await retrieve(question)
    written: list[str] = []

    for _ in range(budget):
        async with aclosing(model.stream(build_prompt(question, context, written))) as parts:
            async for sentence, confidence in sentences_with_confidence(parts):
                if confidence >= THRESHOLD:
                    written.append(sentence)
                    yield attach_citations(sentence, context)
                    continue
                # A low-confidence sentence is not emitted; it becomes a query.
                probe = strip_uncertain_spans(sentence)
                context = merge(context, await retrieve(probe))
                break
            else:
                return                       # the stream ran dry; the answer is complete
    async for sentence in finish_without_lookahead(question, context, written):
        yield attach_citations(sentence, context)
