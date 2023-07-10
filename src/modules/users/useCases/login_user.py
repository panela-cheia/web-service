import jwt

from modules.users.repositories.user_repository import UserRepository
from modules.users.providers.hash import compare

from shared.errors.errors import CustomError

from config.environments import MD5
from utils.serializator.login_user import loginUserSerializator


class LoginUserUseCase:
    def __init__(self, userRepository: UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, email, password):
        try:
            user = self.userRepository.findByEmail(email)
            
            if not user:
                raise CustomError("User not exists")

            if not compare(password, user.password):
                raise CustomError("Password does not match!")

            payload_data = {
                "sub": "4242",
                "id": user.id,
            }

            token = jwt.encode(
                payload=payload_data,
                key=MD5
            )

            response = loginUserSerializator(user=user, token=token)
            return response
        except:
            return {"error": "An error occurred during user login"}
