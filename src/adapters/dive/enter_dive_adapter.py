import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.dive.useCases.enter_dive import EnterDiveUseCase

@Pyro5.server.expose
class EnterDiveAdapter(object):
    def __init__(self) -> None:
        self.useCase = EnterDiveUseCase(repository=DiveRepository())
    
    def execute(self, userId: str, diveId: str):
        dive = self.useCase.execute(user_id=userId, dive_id=diveId)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_ENTER.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_ENTER.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive    
        