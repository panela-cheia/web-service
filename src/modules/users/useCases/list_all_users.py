from modules.users.repositories.user_repository import UserRepository

from utils.serializator.users_all import serialize_user

class ListAllUsersUseCase(object):
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self):
        users = self.userRepository.findAll()

        serialized_users = []

        for user in users:
            serialized_users.append({
                "id":user.id,
                "name":user.name,
                "username":user.username,
                "email":user.email
            })
      
        return serialized_users