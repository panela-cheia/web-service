import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.list_others import ListOthersUseCase

@Pyro5.server.expose
class ListOthersUsersAdapter(object):
    def __init__(self) -> None:
        self.useCase = ListOthersUseCase(userRepository=UserRepository())

    def execute(self,id:str):
        try:
            users = self.useCase.execute(id=id)
            logger.info("{topic} - {user}",topic=Topics.USER_LIST_OTHERS.value,user=json.dumps(users,indent=4,ensure_ascii=False))

            return users    
        except (ValueError):
            return { "error":ValueError }        