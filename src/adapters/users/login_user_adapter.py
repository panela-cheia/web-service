import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.login_user import LoginUserUseCase

@Pyro5.server.expose
class LoginUserAdapter(object):
    def __init__(self) -> None:
        self.useCase = LoginUserUseCase(userRepository=UserRepository())

    def execute(self,email:str,password:str):
        user = self.useCase.execute(email=email,password=password)
        logger.info("{topic} - {user}",topic=Topics.USER_LOGIN_EMAIL.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user