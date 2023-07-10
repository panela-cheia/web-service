from typing import Optional,List
from pydantic import BaseModel

class IngredientDTO(BaseModel):
    name: str
    amount: int
    unit: str

class CreateRecipeDTO(BaseModel):
    name: str
    description: str
    userId: str
    fileId: str
    diveId: Optional[str]
    ingredients: List[IngredientDTO]