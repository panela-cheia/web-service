from pydantic import BaseModel

class CreateDiveDTO(BaseModel):
    name: str
    description: str
    fileId: str
    userId: str