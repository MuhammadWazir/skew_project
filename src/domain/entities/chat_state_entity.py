from typing import List, Optional
from pydantic import BaseModel
from src.domain.entities.chunk_data_entity import ChunkDataEntity


class ChatStateEntity(BaseModel):
    """State entity for LangGraph chat flow"""
    user_query: str
    needs_rag: Optional[bool] = None
    retrieved_chunks: Optional[List[ChunkDataEntity]] = None
    response: Optional[str] = None
    sources: Optional[List[str]] = None

