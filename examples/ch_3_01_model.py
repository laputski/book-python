from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Chunk:
    """Фрагмент корпуса. Внутренний тип: проверка уже пройдена."""
    id: str
    doc_id: str
    text: str
    context: str = ""            # приписанный контекстный префикс
    start: int = 0               # смещение в исходном документе
    end: int = 0

    @property
    def embedding_input(self) -> str:
        return f"{self.context}\n\n{self.text}" if self.context else self.text

@dataclass(frozen=True, slots=True)
class Scored:
    chunk: Chunk
    score: float
    source: str                  # имя источника, породившего кандидата
