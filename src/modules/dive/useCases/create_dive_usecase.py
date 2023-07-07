from modules.dive.dtos.create_dive_dto import CreateDiveDTO
from modules.dive.repositories.dive_repository import DiveRepository

class CreateDiveUseCase:
    def __init__(self, repository: DiveRepository) -> None:
        self.repository = repository
    
    def execute(self, data:CreateDiveDTO):

        try:
            dive = self.repository.create(data=data)
            self.repository.enterDive(dive_id=dive.id,user_id=data.userId)

            return { "ok": "dive created!" }
        except (ValueError):
            return { "error": ValueError }