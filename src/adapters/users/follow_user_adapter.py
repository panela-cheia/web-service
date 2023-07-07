import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.follow_user import FollowUserUseCase

@Pyro5.server.expose
class FollowUserAdapter(object):
    def __init__(self) -> None:
        self.useCase = FollowUserUseCase(userRepository=UserRepository())

    def execute(self,user_id:str,follow_id:str):
        user = self.useCase.execute(user_id=follow_id,follow_id=user_id)

        if "error" in user:
            logger.error("{topic} - {user}",topic=Topics.USER_FOLLOW.value,user=json.dumps(user,indent=4,ensure_ascii=False))
            
        else:
            logger.info("{topic} - {user}",topic=Topics.USER_FOLLOW.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user