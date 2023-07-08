import Pyro5.server

# repositories
from modules.files.repositories.files_repository import FilesRepository

# useCase
from modules.files.useCases.find_file_by_name import FindFileByName

@Pyro5.server.expose
class FindFileByNameAdapter(object):
    def __init__(self) -> None:
        self.useCase = FindFileByName(repository=FilesRepository())

    def execute(self,filename:str):
        archive = self.useCase.execute(filename=filename)

        return archive