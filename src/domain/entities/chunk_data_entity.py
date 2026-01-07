from pydantic import BaseModel

class ChunkDataEntity(BaseModel):
    filename: str
    chunk_index: int
    text: str
    score: float