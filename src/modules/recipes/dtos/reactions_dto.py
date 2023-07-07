from enum import Enum
from pydantic import BaseModel

class ReactionType(str, Enum):
    BAO = "bão"
    MIO_DE_BAO = "mió de bão"
    AGUA_NA_BOCA = "água na boca"

class ReactionDTO(BaseModel):
    type: ReactionType
    recipe_id: str
    user_id: str