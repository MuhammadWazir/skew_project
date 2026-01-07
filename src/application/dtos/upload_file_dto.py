from pydantic import BaseModel

class UploadFileDTO(BaseModel):
    filename: str
    file: bytes