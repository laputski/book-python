from pydantic import BaseModel

class Chunk(BaseModel):
    id: str
    doc_id: str
    text: str
    context: str = ""

class Scored(BaseModel):
    chunk: Chunk           # проверяется заново при каждом создании
    score: float
    source: str
