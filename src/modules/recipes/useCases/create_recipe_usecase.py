from modules.recipes.repositories.recipe_repository import RecipeRepository
from modules.recipes.dtos.create_recipe_dto import CreateRecipeDTO

class CreateRecipeUseCase:
    def __init__(self,repository:RecipeRepository) -> None:
        self.repository = repository

    def execute(self,data:CreateRecipeDTO):

        try:
            recipe =  self.repository.create(data=data)

            if not recipe:
                raise Exception("Error to try create recipe!")

            data = {
                "ok":"recipe created successfully!"
            }

            return data
        except (ValueError):
            return {"error":ValueError}