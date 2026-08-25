from typing import Annotated, Literal
from pydantic import BaseModel, Field

class DraftScore(BaseModel):
    draft_index: Annotated[int, Field(ge=0, description="номер черновика")]
    supported: Annotated[bool, Field(description="опирается ли на приведённые фрагменты")]
    score: Annotated[float, Field(ge=0.0, le=1.0, description="пригодность ответа")]
    problem: Annotated[str | None, Field(default=None, max_length=200,
                                        description="что именно не так, если не так")]

class Verdict(BaseModel):
    """Оценка черновиков и выбор лучшего."""
    scores: Annotated[list[DraftScore], Field(min_length=1, max_length=8)]
    chosen: Annotated[int, Field(ge=0, description="номер выбранного черновика")]
    decision: Literal["accept", "reject", "need_more_context"]

SCHEMA = Verdict.model_json_schema()      # тот же источник, что и проверка
