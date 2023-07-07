from modules.users.repositories.user_repository import UserRepository
from utils.serializator.search_uses import searchUsersSerializator

class SearchUsersUseCase:
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self,user_id:str,value:str):
        users = self.userRepository.searchUser(user_id=user_id,value=value)

        results = [ ]

        print(users)

        for user in users:
            print(user)
            results.append(searchUsersSerializator(user))

        return results