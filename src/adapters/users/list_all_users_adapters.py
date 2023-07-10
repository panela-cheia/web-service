import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.list_all_users import ListAllUsersUseCase

@Pyro5.server.expose
class ListAllUsersAdapter(object):
    def __init__(self) -> None:
        self.useCase = ListAllUsersUseCase(userRepository=UserRepository())

    def execute(self):
        try:
            users = self.useCase.execute()
            logger.info("{topic} - {user}",topic=Topics.USER_LIST.value,user=json.dumps(users,indent=4,ensure_ascii=False))

            return users    
        except (ValueError):
            return { "error":ValueError }        