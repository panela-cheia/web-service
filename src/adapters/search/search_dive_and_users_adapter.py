import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.users.repositories.user_repository import UserRepository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.search.useCases.search_dive_and_users_usecase import SearchDiveAndUserUseCase,SearchDiveAndUserDTO

@Pyro5.server.expose
class SearchDiveAndUsersAdapter(object):
    def __init__(self) -> None:
        self.useCase = SearchDiveAndUserUseCase(diveRepository=DiveRepository(),userRepository=UserRepository())

    def execute(self,user_id:str,search_value:str):
        
        dto = SearchDiveAndUserDTO(
            search_value=search_value,
            user_id=user_id
        )

        search = self.useCase.execute(data=dto)
        
        if "error" in search:
            logger.error("{topic} - {response}",topic=Topics.SEARCH_DIVE_AND_USERS.value,response=json.dumps(search,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.SEARCH_DIVE_AND_USERS.value,response=json.dumps(search,indent=4,ensure_ascii=False))

        return search