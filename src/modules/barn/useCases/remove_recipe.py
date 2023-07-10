from modules.barn.dtos.remove_recipe_dto import RemoveRecipeDTO
from modules.barn.repositories.barn_repository import BarnRepository


class RemoveRecipeUseCase:
    def __init__(self, repository: BarnRepository):
        self.repository = repository

    def execute(self, data: RemoveRecipeDTO):
        try:
            barn =  self.repository.removeRecipe(data=data)

            if not barn:
                raise ValueError("User does not exist") 

            response = {"ok":"removed in barn!"}

            return response
        except (ValueError):
            return {"error": ValueError}