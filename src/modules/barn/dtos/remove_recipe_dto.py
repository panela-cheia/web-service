from pydantic import BaseModel

class RemoveRecipeDTO(BaseModel):
    barnId: str
    recipeId: str