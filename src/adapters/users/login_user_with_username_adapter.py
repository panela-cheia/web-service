import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.login_user_with_username import LoginUserWithUsernameUseCase

@Pyro5.server.expose
class LoginUserWithUsernameAdapter(object):
    def __init__(self) -> None:
        self.useCase = LoginUserWithUsernameUseCase(userRepository=UserRepository())

    def execute(self,username:str,password:str):
        user = self.useCase.execute(username=username,password=password)
        logger.info("{topic} - {user}",topic=Topics.USER_LOGIN_EMAIL.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user