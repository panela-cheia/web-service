from pydantic import BaseModel

class SearchRecipeInBarnDTO(BaseModel):
    barnId : str
    recipeName : str