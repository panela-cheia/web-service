import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository
from modules.barn.repositories.barn_repository import BarnRepository

# useCase
from modules.users.useCases.users_barn import UsersBarnUseCase

@Pyro5.server.expose
class UserBarnAdapter(object):
    def __init__(self) -> None:
        self.useCase = UsersBarnUseCase(userRepository=UserRepository(),barnRepository=BarnRepository())

    def execute(self):
        user_id="6809d450-68e0-479f-91e1-7d2d5c52ad90"

        user = self.useCase.execute(user_id=user_id)
    
        logger.info("{topic} - {user}",topic=Topics.USER_BARN.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user