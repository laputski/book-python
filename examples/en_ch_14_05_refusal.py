from typing import Self

from pydantic import BaseModel, Field, model_validator

class Extraction(BaseModel):
    """Extracting a fact from a chunk. The fact's absence is itself an answer."""
    found: bool
    value: str | None = None
    quote: str | None = Field(default=None, description="a verbatim excerpt")

    @model_validator(mode="after")
    def coherent(self) -> Self:
        if self.found and not (self.value and self.quote):
            raise ValueError("found=true requires a value and a quote")
        if not self.found and (self.value or self.quote):
            raise ValueError("found=false admits neither value nor quote")
        return self
