from pydantic import BaseModel

class Chunk(BaseModel):
    id: str
    doc_id: str
    text: str
    context: str = ""

class Scored(BaseModel):
    chunk: Chunk           # re-validated on every construction
    score: float
    source: str
