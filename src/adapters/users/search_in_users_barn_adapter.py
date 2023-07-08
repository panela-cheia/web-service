import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository
from modules.barn.repositories.barn_repository import BarnRepository

# useCase
from modules.users.useCases.search_in_users_barn import SearchInUsersBarnUseCase

@Pyro5.server.expose
class SearchInUsersBarnAdapter(object):
    def __init__(self) -> None:
        self.useCase = SearchInUsersBarnUseCase(userRepository=UserRepository(),barnRepository=BarnRepository())

    def execute(self,user_id:str,value:str):
        user = self.useCase.execute(user_id=user_id,value=value)
        
        logger.info("{topic} - {user}",topic=Topics.USER_LOGIN_EMAIL.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user