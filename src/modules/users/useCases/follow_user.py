import jwt
import json

from modules.users.repositories.user_repository import UserRepository


from shared.errors.errors import CustomError

class FollowUserUseCase:
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, user_id: str, follow_id: str):
        # Verificar se o usuário existe
        user = self.userRepository.findById(id=user_id)
        if not user:
            return { "error":"User does not exist" }

        # Verificar se o usuário está tentando seguir a si mesmo
        if user_id == follow_id:
            return { "error":"Cannot follow yourself" }

        # Verificar se o usuário a ser seguido existe
        follow_user = self.userRepository.findById(id=follow_id)
        if not follow_user:
            return { "error": "User to follow does not exist" }

        # Verificar se o usuário já está seguindo o usuário a ser seguido
        existing_follow = self.userRepository.verifyFollowing(follower=user_id,following=follow_id)
        
        if existing_follow:
            return { "error":"Already following this user" }

        # Criar o relacionamento de seguir
        self.userRepository.followUser(user_id=user_id,follow_id=follow_id)
        
        return { "ok":"Successfully followed user" }