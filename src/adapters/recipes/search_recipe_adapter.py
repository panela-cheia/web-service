import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.recipes.repositories.recipe_repository import RecipeRepository

# useCase
from modules.recipes.useCases.search_recipes_usecase import SearchRecipesUseCase


@Pyro5.server.expose
class SearchRecipeAdapter(object):
    def __init__(self) -> None:
        self.useCase = SearchRecipesUseCase(repository=RecipeRepository())

    def execute(self,name:str):
        
        recipe = self.useCase.execute(name=name)
        
        if "error" in recipe:
            logger.error("{topic} - {response}",topic=Topics.RECIPE_SEARCH.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.RECIPE_SEARCH.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))

        return recipe