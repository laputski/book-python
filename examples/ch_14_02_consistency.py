# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import DraftScore  # noqa: F401
# ─── листинг ───
from typing import Self

from pydantic import BaseModel, model_validator

class Verdict(BaseModel):
    scores: list[DraftScore]      # объявлены выше, повторены ради ясности
    chosen: int

    @model_validator(mode="after")
    def chosen_must_exist(self) -> Self:
        known = {s.draft_index for s in self.scores}
        if self.chosen not in known:
            raise ValueError(f"выбран черновик {self.chosen}, оценки для него нет")
        return self
