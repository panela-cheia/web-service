from modules.recipes.repositories.recipe_repository import RecipeRepository
from utils.serializator.recipe_without_reactions import recipeWithoutReactionsSerializator

class SearchRecipesUseCase:
    def __init__(self,repository:RecipeRepository) -> None:
        self.repository = repository

    def execute(self,name:str):
        recipes =  self.repository.search(name=name)
        
        data = []

        for recipe in recipes:
            data.append(recipeWithoutReactionsSerializator(recipe=recipe))

        return data