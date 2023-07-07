import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.update_photo_user import UpdatePhotoUserUseCase

@Pyro5.server.expose
class UpdatePhotoUserAdapter(object):
    def __init__(self) -> None:
        self.useCase = UpdatePhotoUserUseCase(userRepository=UserRepository())

    def execute(self,id:str,photo:str):
        user = self.useCase.execute(id=id,photo=photo)

        logger.info("{topic} - {user}",topic=Topics.USER_UNFOLLOW.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user