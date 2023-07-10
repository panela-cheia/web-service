from pydantic import BaseModel

class CreateFileDTO(BaseModel):
    name: str
    path: str