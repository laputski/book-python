from pydantic import BaseModel, Field, model_validator

class Extraction(BaseModel):
    """Извлечение сведения из фрагмента. Отсутствие сведения является ответом."""
    found: bool
    value: str | None = None
    quote: str | None = Field(default=None, description="дословная выдержка")

    @model_validator(mode="after")
    def coherent(self) -> "Extraction":
        if self.found and not (self.value and self.quote):
            raise ValueError("при found=true требуются значение и выдержка")
        if not self.found and (self.value or self.quote):
            raise ValueError("при found=false значение и выдержка недопустимы")
        return self
