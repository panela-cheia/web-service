import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.recipes.repositories.recipe_repository import RecipeRepository

# useCase
from modules.recipes.useCases.create_recipe_usecase import CreateRecipeUseCase,CreateRecipeDTO

from utils.convert_list_convert_to_ingredient_dtos import convert_list_to_ingredient_dtos

@Pyro5.server.expose
class CreateRecipeAdapter(object):
    def __init__(self) -> None:
        self.useCase = CreateRecipeUseCase(repository=RecipeRepository())

    def execute(self,name:str,description:str,ingredients:list,userId:str,fileId:str,diveId:str):
        dto = CreateRecipeDTO(
            name=name,
            description=description,
            ingredients=convert_list_to_ingredient_dtos(data=ingredients),
            userId=userId,
            fileId=fileId,
            diveId=diveId if "diveId" else None
        )
        
        recipe = self.useCase.execute(data=dto)
        
        if "error" in recipe:
            logger.error("{topic} - {response}",topic=Topics.RECIPE_CREATE.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.RECIPE_CREATE.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))

        return recipe