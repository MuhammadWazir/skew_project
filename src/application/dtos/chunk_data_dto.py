from pydantic import BaseModel

class ChunkDataDTO(BaseModel):
    filename: str
    chunk_index: int
    text: str
    score: float