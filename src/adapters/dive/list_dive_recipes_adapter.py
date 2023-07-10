import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository
from modules.recipes.repositories.recipe_repository import RecipeRepository

# useCase
from modules.dive.useCases.list_dive_recipes_usecase import ListDiveRecipesUseCase

@Pyro5.server.expose
class ListDiveRecipeAdapter(object):
    def __init__(self) -> None:
        self.useCase = ListDiveRecipesUseCase(repository=DiveRepository(), recipeRepository=RecipeRepository())
    
    def execute(self, diveId:str):
        dive = self.useCase.execute(dive_id=diveId)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_LIST_RECIPES.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_LIST_RECIPES.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive