from modules.users.repositories.user_repository import UserRepository
from modules.users.dtos.update_user_dto import UpdateUserDTO

from shared.errors.errors import CustomError

class UpdatePhotoUserUseCase:
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, id:str,photo: str):
        try:
            user = self.userRepository.updatePhoto(
                id=id,
                photo_id=photo
            )

            print(user.__dict__)

            return { "ok":"Successfully updated user: " }
        except:
            raise { "error": "An error occurred during user creation" }