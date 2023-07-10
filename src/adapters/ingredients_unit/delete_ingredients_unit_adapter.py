import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.ingredients_unit.repositories.ingredients_unit_repository import IngredientsUnitRepository

# useCase
from modules.ingredients_unit.useCases.delete_ingredients_unit_usecase import DeleleIngredientsUnitUseCase

@Pyro5.server.expose
class DeleteIngredientsUnitAdapter(object):
    def __init__(self) -> None:
        self.useCase = DeleleIngredientsUnitUseCase(repository=IngredientsUnitRepository())

    def execute(self,id:str):
        ingredient = self.useCase.execute(id=id)
        
        if "error" in ingredient:
            logger.error("{topic} - {response}",topic=Topics.INGREDIENT_UNIT_DELETE.value,response=json.dumps(ingredient,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.INGREDIENT_UNIT_DELETE.value,response=json.dumps(ingredient,indent=4,ensure_ascii=False))
        
        return ingredient