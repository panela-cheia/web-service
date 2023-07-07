import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.dive.useCases.list_users_dive import ListUserDiveUseCase

@Pyro5.server.expose
class ListUsersAdapter(object):
    def __init__(self) -> None:
        self.useCase = ListUserDiveUseCase(repository=DiveRepository())
        
    def execute(self, userId:str):
        dive = self.useCase.execute(user_id=userId)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_USERS_DIVE.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_USERS_DIVE.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive