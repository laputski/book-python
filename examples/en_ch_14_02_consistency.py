# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import DraftScore  # noqa: F401
# ─── листинг ───
from typing import Self

from pydantic import BaseModel, model_validator

class Verdict(BaseModel):
    scores: list[DraftScore]      # declared above; repeated for clarity
    chosen: int

    @model_validator(mode="after")
    def chosen_must_exist(self) -> Self:
        known = {s.draft_index for s in self.scores}
        if self.chosen not in known:
            raise ValueError(f"draft {self.chosen} was chosen, but no score exists for it")
        return self
