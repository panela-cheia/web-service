import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.dive.useCases.update_dive import UpdateDiveUseCase, UpdateDiveDTO

@Pyro5.server.expose
class UpdateDiveAdapter(object):
    def __init__(self) -> None:
        self.useCase = UpdateDiveUseCase(repository=DiveRepository())
        
    def execute(self, id: str, name: str, description: str, fileId: str):
        dto = UpdateDiveDTO(
            id=id,
            name=name if "name" else None,
            description=description if "description" else None,
            fileId=fileId if "fileId" else None
        )
        
        dive = self.useCase.execute(updateDiveDTO=dto)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_UPDATE.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_UPDATE.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive