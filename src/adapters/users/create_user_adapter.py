import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository

# useCase
from modules.users.useCases.create_user import CreateUserUseCase,CreateUserDTO

@Pyro5.server.expose
class CreateUserAdapter(object):
    def __init__(self) -> None:
        self.useCase = CreateUserUseCase(userRepository=UserRepository())

    def execute(self,name:str,username:str,email:str,password:str):
        dto = CreateUserDTO(
            name=name,
            username=username,
            email=email,
            password=password,

        )
        
        user = self.useCase.execute(createUserDTO=dto)
        
        if "error" in user:
            logger.error("{topic} - {user}",topic=Topics.USER_CREATE.value,user=json.dumps(user,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {user}",topic=Topics.USER_CREATE.value,user=json.dumps(user,indent=4,ensure_ascii=False))

        return user