import jwt
import json

from modules.users.repositories.user_repository import UserRepository
from providers.hash import compare

from config.environments import MD5
from utils.serializator.login_user import loginUserSerializator

class LoginUserWithUsernameUseCase:
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, username,password):
        try:
            user = self.userRepository.findByUsername(username)

            if not user:
                return { "error": "User not exists" }

            if not compare(password,user.password):
                return { "error": "Password does not match!" }

            payload_data = {
                "sub": "4242",
                "id": user.id,
            }

            token = jwt.encode(
                payload=payload_data,
                key=MD5
            )

            response = loginUserSerializator(user=user,token=token)
            return response
    
        except:
            return { "error":"An error occurred during user login" }