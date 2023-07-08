from modules.files.repositories.files_repository import FilesRepository

#from shared.errors.errors import CustomError

class FindFileByName:
    def __init__(self, repository: FilesRepository) -> None:
        self.repository = repository

    def execute(self, filename:str):
        response = self.repository.findByName(name=filename)

        print(response)

        data = {
            "id": response.id,
            "name": response.name,
            "path": response.path
        }

        return data 