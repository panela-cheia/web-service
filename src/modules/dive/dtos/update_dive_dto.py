from pydantic import BaseModel
from typing import Optional

class UpdateDiveDTO(BaseModel):
    id: str
    name: Optional[str]
    description: Optional[str]
    fileId: Optional[str]