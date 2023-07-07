import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.dive.useCases.search_dive import SearchDiveUseCase

@Pyro5.server.expose
class SearchDiveAdapter(object):
    def __init__(self) -> None:
        self.useCase = SearchDiveUseCase(repository=DiveRepository())
    
    def execute(self, diveName:str):
        dive = self.useCase.execute(diveName=diveName)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_SEARCH.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_SEARCH.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive
        