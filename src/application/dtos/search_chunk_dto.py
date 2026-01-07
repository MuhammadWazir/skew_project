from pydantic import BaseModel

class SearchChunkDTO(BaseModel):
    query: str