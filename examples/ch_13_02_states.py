# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored  # noqa: F401
# --- the listing ---
from dataclasses import dataclass
from typing import Literal, assert_never

@dataclass(frozen=True, slots=True)
class Budget:
    steps: int = 4
    tokens: int = 12_000
    spent_steps: int = 0
    spent_tokens: int = 0

    @property
    def exhausted(self) -> bool:
        return self.spent_steps >= self.steps or self.spent_tokens >= self.tokens

@dataclass(frozen=True, slots=True)
class Classify:
    kind: Literal["classify"] = "classify"
    question: str = ""

@dataclass(frozen=True, slots=True)
class Retrieve:
    kind: Literal["retrieve"] = "retrieve"
    query: str = ""
    context: tuple[Scored, ...] = ()

@dataclass(frozen=True, slots=True)
class Generate:
    kind: Literal["generate"] = "generate"
    context: tuple[Scored, ...] = ()

@dataclass(frozen=True, slots=True)
class Critique:
    kind: Literal["critique"] = "critique"
    draft: str = ""
    context: tuple[Scored, ...] = ()

@dataclass(frozen=True, slots=True)
class Answer:
    kind: Literal["answer"] = "answer"
    text: str = ""
    partial: bool = False

State = Classify | Retrieve | Generate | Critique | Answer
