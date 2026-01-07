from pydantic import BaseModel


class ChatRequestDTO(BaseModel):
    message: str

