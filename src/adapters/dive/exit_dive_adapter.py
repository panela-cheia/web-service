import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repository
from modules.dive.repositories.dive_repository import DiveRepository

# useCase
from modules.dive.useCases.exit_dive import ExitDiveUseCase, ExitDiveDTO

@Pyro5.server.expose
class ExitDiveAdapter(object):
    def __init__(self) -> None:
        self.useCase = ExitDiveUseCase(repository=DiveRepository())
    
    def execute(self, user: str, new_owner: str, diveId: str):
        dto = ExitDiveDTO(
            user=user,
            new_owner=new_owner if "new_owner" else None,
            diveId=diveId
        )
        
        dive = self.useCase.execute(data=dto)
        
        if "error" in dive:
            logger.error("{topic} - {dive}", topic=Topics.DIVE_EXIT.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
        else:
            logger.info("{topic} - {dive}", topic=Topics.DIVE_EXIT.value, dive=json.dumps(dive, indent=4, ensure_ascii=False))
            
        return dive