from pydantic import BaseModel
from typing import Optional

class UpdateUserDTO(BaseModel):
    name: str
    username: str
    bio: str