from pydantic import BaseModel
from typing import Optional

class ExitDiveDTO(BaseModel):
    user: str
    new_owner: Optional[str]
    diveId: str