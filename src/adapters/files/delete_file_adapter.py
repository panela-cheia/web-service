import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.files.repositories.files_repository import FilesRepository

# useCase
from modules.files.useCases.delete_file import DeleteFileUseCase,DeleteFileDTO

@Pyro5.server.expose
class DeleteFileAdapter(object):
    def __init__(self) -> None:
        self.useCase = DeleteFileUseCase(repository=FilesRepository())

    def execute(self,id:str):
        dto = DeleteFileDTO(
            id=id
        )
        
        archive = self.useCase.execute(deleteFileDTO=dto)
        
        if "error" in archive:
            logger.error("{topic} - {response}",topic=Topics.FILE_DELETE.value,response=json.dumps(archive,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.FILE_DELETE.value,response=json.dumps(archive,indent=4,ensure_ascii=False))

        return archive