import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.files.repositories.files_repository import FilesRepository

# useCase
from modules.files.useCases.create_file import CreateFileUseCase,CreateFileDTO

@Pyro5.server.expose
class CreateFileAdapter(object):
    def __init__(self) -> None:
        self.useCase = CreateFileUseCase(repository=FilesRepository())

    def execute(self,name:str,path:str):
        dto = CreateFileDTO(
            name=name,
            path=path
        )
        
        archive = self.useCase.execute(createFileDTO=dto)
        
        if "error" in archive:
            logger.error("{topic} - {response}",topic=Topics.FILE_CREATE.value,response=json.dumps(archive,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.FILE_CREATE.value,response=json.dumps(archive,indent=4,ensure_ascii=False))
        
        return archive