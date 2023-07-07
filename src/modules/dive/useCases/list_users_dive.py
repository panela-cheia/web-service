from modules.dive.repositories.dive_repository import DiveRepository
from utils.serializator.users_dive import usersDiveSerializator


class ListUserDiveUseCase:
    def __init__(self, repository: DiveRepository) -> None:
        self.repository = repository

    def execute(self, user_id: str):
        dives = self.repository.findUserDive(user_id=user_id)

        final_dives = []
        for dive in dives:
            final_dives.append(usersDiveSerializator(dive=dive))
        return final_dives