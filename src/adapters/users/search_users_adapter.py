import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.search_users import SearchUsersUseCase

@Pyro5.server.expose
class SearchUsersAdapter(object):
    def __init__(self) -> None:
        self.useCase = SearchUsersUseCase(userRepository=UserRepository())

    def execute(self,user_id:str,value:str):
        user = self.useCase.execute(user_id=user_id,value=value)

        logger.info("{topic} - {user}",topic=Topics.USER_SEARCH_USERS.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user