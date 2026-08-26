# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Answer, Budget, Classify, Critique, Generate, Retrieve, State, generate, grounded, route, search, spend  # noqa: F401
# ─── листинг ───
from typing import assert_never

async def step(state: State, budget: Budget) -> tuple[State, Budget]:
    match state:
        case Classify(question=q):
            match await route(q):
                case "simple":
                    return Generate(context=()), budget
                case "single":
                    return Retrieve(query=q), budget
                case "multi":
                    return Retrieve(query=q), budget
                case other:
                    raise ValueError(f"unknown class {other!r}")

        case Retrieve(query=q, context=ctx):
            found = await search(q)
            return Generate(context=ctx + tuple(found)), spend(budget, steps=1)

        case Generate(context=ctx):
            draft = await generate(ctx)
            return Critique(draft=draft, context=ctx), spend(budget, tokens=len(draft))

        case Critique(draft=d, context=ctx) if budget.exhausted:
            return Answer(text=d, partial=True), budget

        case Critique(draft=d, context=ctx):
            verdict = await grounded(d, ctx)
            if verdict.ok:
                return Answer(text=d), budget
            return Retrieve(query=verdict.probe, context=ctx), budget

        case Answer():
            return state, budget

        case _:
            assert_never(state)
