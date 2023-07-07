import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.ingredients_unit.repositories.ingredients_unit_repository import IngredientsUnitRepository

# useCase
from modules.ingredients_unit.useCases.list_ingredients_unit_usecase import ListIngredientsUnitUseCase

@Pyro5.server.expose
class ListIngredientsUnitAdapter(object):
    def __init__(self) -> None:
        self.useCase = ListIngredientsUnitUseCase(repository=IngredientsUnitRepository())

    def execute(self):
        ingredient = self.useCase.execute()
        
        if "error" in ingredient:
            logger.error("{topic} - {response}",topic=Topics.INGREDIENT_UNI_CREATE.value,response=json.dumps(ingredient,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.INGREDIENT_UNI_CREATE.value,response=json.dumps(ingredient,indent=4,ensure_ascii=False))
        
        return ingredient