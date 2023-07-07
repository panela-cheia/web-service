from modules.users.repositories.user_repository import UserRepository

from utils.serializator.users_all import serialize_user

class ListOthersUseCase:
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self,id:str):
        verifyIfUserExists =  self.userRepository.findById(id)

        if not verifyIfUserExists:
            raise ValueError("Invalid user ID")
            
        users = self.userRepository.findOther(id)

        serialized_users = []

        for user in users:
            serialized_users.append(serialize_user(user))

        return serialized_users