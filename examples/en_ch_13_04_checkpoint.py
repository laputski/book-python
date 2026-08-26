# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Answer, Budget, Classify, Critique, Generate, Retrieve, State  # noqa: F401
# ─── листинг ───
import json
from dataclasses import asdict

STATES: dict[str, type[State]] = {
    "classify": Classify, "retrieve": Retrieve, "generate": Generate,
    "critique": Critique, "answer": Answer,
}

def dump(state: State, budget: Budget) -> str:
    return json.dumps({"state": asdict(state), "budget": asdict(budget)},
                      ensure_ascii=False)

def load(raw: str) -> tuple[State, Budget]:
    data = json.loads(raw)
    payload = data["state"]
    cls = STATES[payload["kind"]]           # the discriminator picks the class
    return cls(**payload), Budget(**data["budget"])
