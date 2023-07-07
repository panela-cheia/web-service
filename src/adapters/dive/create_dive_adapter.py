import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.dive.useCases.create_dive_usecase import CreateDiveUseCase, CreateDiveDTO

@Pyro5.server.expose
class CreateDiveAdapter(object):
    def __init__(self) -> None:
        self.useCase = CreateDiveUseCase(repository=DiveRepository())
    
    def execute(self, name: str, description: str, fileId: str, userId: str):
        dto = CreateDiveDTO(
            name=name,
            description=description,
            fileId=fileId,
            userId=userId
        )
        
        dive = self.useCase.execute(data=dto)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_CREATE.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_CREATE.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive