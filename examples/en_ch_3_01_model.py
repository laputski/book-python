from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Chunk:
    """A corpus chunk. An internal type: validation has already happened."""
    id: str
    doc_id: str
    text: str
    context: str = ""            # the attached context prefix
    start: int = 0               # offset in the source document
    end: int = 0

    @property
    def embedding_input(self) -> str:
        return f"{self.context}\n\n{self.text}" if self.context else self.text

@dataclass(frozen=True, slots=True)
class Scored:
    chunk: Chunk
    score: float
    source: str                  # the name of the source that produced the candidate
