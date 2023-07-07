import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.update_user import UpdateUserUseCase, UpdateUserDTO


@Pyro5.server.expose
class UpdateUserAdapter(object):
    def __init__(self) -> None:
        self.useCase = UpdateUserUseCase(userRepository=UserRepository())

    def execute(self, id: str, name: str, username: str, bio: str):
        dto = UpdateUserDTO(
            name=name, bio=bio, username=username
        )

        user = self.useCase.execute(id=id, updateUserDTO=dto)

        logger.info("{topic} - {user}", topic=Topics.USER_UPDATE.value,
                    user=json.dumps(user, indent=4, ensure_ascii=False))

        return user
