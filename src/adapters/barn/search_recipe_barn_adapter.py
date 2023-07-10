import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.barn.repositories.barn_repository import BarnRepository

# useCase
from modules.barn.useCases.search_recipe import SearhRecipeUseCase, SearchRecipeInBarnDTO

@Pyro5.server.expose
class SearchRecipeBarnAdapter(object):
    def __init__(self) -> None:
        self.useCase = SearhRecipeUseCase(repository=BarnRepository())

    def execute(self, barnId: str, recipeName: str):
        dto = SearchRecipeInBarnDTO(
            barnId=barnId,
            recipeName=recipeName
        )
        
        barn = self.useCase.execute(data=dto)
        
        if "error" in barn:
            logger.error("{topic} - {barn}", topic=Topics.BARN_SEARCH_RECIPE.value, barn=json.dumps(barn, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {barn}", topic=Topics.BARN_SEARCH_RECIPE.value, barn=json.dumps(barn, indent=4, ensure_ascii=False))
            
        return barn