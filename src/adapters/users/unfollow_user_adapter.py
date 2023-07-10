import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.unfollow_user import UnfollowUserUseCase

@Pyro5.server.expose
class UnfollowUserAdapter(object):
    def __init__(self) -> None:
        self.useCase = UnfollowUserUseCase(userRepository=UserRepository())

    def execute(self,user_id:str,unfollow_id:str):
        user = self.useCase.execute(user_id=unfollow_id,unfollow_id=user_id)

        logger.info("{topic} - {user}",topic=Topics.USER_UNFOLLOW.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user