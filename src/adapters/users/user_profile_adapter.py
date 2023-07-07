import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.user_profile import UserProfileUseCase


@Pyro5.server.expose
class UserProfileAdapter(object):
    def __init__(self) -> None:
        self.useCase = UserProfileUseCase(userRepository=UserRepository())

    def execute(self, user_id: str):
        user = self.useCase.execute(user_id=user_id)

        if "error" in user:
            logger.error("{topic} - {user}", topic=Topics.USER_PROFILE.value,
                    user=json.dumps(user, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {user}", topic=Topics.USER_UPDATE.value,
                    user=json.dumps(user, indent=4, ensure_ascii=False))

        return user
