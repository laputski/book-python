from typing import Annotated, Literal
from pydantic import BaseModel, Field

class DraftScore(BaseModel):
    draft_index: Annotated[int, Field(ge=0, description="the draft's index")]
    supported: Annotated[bool, Field(description="whether it rests on the given chunks")]
    score: Annotated[float, Field(ge=0.0, le=1.0, description="the answer's fitness")]
    problem: Annotated[str | None, Field(default=None, max_length=200,
                                        description="what exactly is wrong, if anything")]

class Verdict(BaseModel):
    """Scoring the drafts and choosing the best."""
    scores: Annotated[list[DraftScore], Field(min_length=1, max_length=8)]
    chosen: Annotated[int, Field(ge=0, description="the chosen draft's index")]
    decision: Literal["accept", "reject", "need_more_context"]

SCHEMA = Verdict.model_json_schema()      # the same source as the validation
