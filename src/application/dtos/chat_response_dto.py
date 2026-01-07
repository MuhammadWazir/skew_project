from typing import List, Optional
from pydantic import BaseModel


class ChatResponseDTO(BaseModel):
    response: str
    sources: Optional[List[str]] = None

