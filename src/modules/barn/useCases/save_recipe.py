from modules.barn.dtos.save_recipe_dto import BarnSaveRecipeDTO
from modules.barn.repositories.barn_repository import BarnRepository


class SaveRecipeUseCase:
    def __init__(self, repository: BarnRepository):
        self.repository = repository

    def execute(self, data: BarnSaveRecipeDTO):
        try:
            barn =  self.repository.save(data=data)

            if not barn:
                raise ValueError("User does not exist") 

            response = {"ok":"saved in barn!"}

            return response
        except (ValueError):
            return {"error":ValueError}