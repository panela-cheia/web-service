import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.recipes.repositories.recipe_repository import RecipeRepository

# useCase
from modules.recipes.useCases.list_usecase import ListRecipesUseCase

@Pyro5.server.expose
class ListRecipeAdapter(object):
    def __init__(self) -> None:
        self.useCase = ListRecipesUseCase(repository=RecipeRepository())

    def execute(self):
        
        recipe = self.useCase.execute()
        
        if "error" in recipe:
            logger.error("{topic} - {response}",topic=Topics.RECIPE_LIST.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.RECIPE_LIST.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))

        return recipe