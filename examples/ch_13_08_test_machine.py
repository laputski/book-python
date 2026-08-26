# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Answer, Budget, Classify, Critique, Generate, Retrieve, step  # noqa: F401
# --- the listing ---
import pytest

@pytest.mark.asyncio
async def test_exhausted_budget_gives_partial_answer() -> None:
    state = Critique(draft="черновик", context=())
    budget = Budget(steps=4, spent_steps=4)

    nxt, _ = await step(state, budget)

    assert isinstance(nxt, Answer)
    assert nxt.partial is True

@pytest.mark.asyncio
async def test_no_state_is_terminal_except_answer() -> None:
    """Из любого состояния, кроме конечного, есть выход при исчерпанном бюджете."""
    budget = Budget(steps=0, spent_steps=1)
    for state in (Classify(), Retrieve(), Generate(), Critique()):
        nxt, _ = await step(state, budget)
        assert nxt != state, f"состояние {type(state).__name__} не продвигается"
