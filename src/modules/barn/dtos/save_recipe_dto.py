from pydantic import BaseModel

class BarnSaveRecipeDTO(BaseModel):
    barnId: str
    recipeId: str
