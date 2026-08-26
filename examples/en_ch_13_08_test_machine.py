# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Answer, Budget, Classify, Critique, Generate, Retrieve, step  # noqa: F401
# ─── листинг ───
import pytest

@pytest.mark.asyncio
async def test_exhausted_budget_gives_partial_answer() -> None:
    state = Critique(draft="a draft", context=())
    budget = Budget(steps=4, spent_steps=4)

    nxt, _ = await step(state, budget)

    assert isinstance(nxt, Answer)
    assert nxt.partial is True

@pytest.mark.asyncio
async def test_no_state_is_terminal_except_answer() -> None:
    """Every state but the final one has an exit when the budget is spent."""
    budget = Budget(steps=0, spent_steps=1)
    for state in (Classify(), Retrieve(), Generate(), Critique()):
        nxt, _ = await step(state, budget)
        assert nxt != state, f"state {type(state).__name__} does not advance"
