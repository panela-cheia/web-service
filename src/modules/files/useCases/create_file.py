from modules.files.repositories.files_repository import FilesRepository
from modules.files.dtos.create_file_dto import CreateFileDTO

from shared.errors.errors import CustomError

from providers.uuid import generate

class CreateFileUseCase:
    def __init__(self,repository:FilesRepository) -> None:
        self.repository = repository

    def execute(self,createFileDTO:CreateFileDTO):
        extension = createFileDTO.name[-4:]

        if extension != ".png" and extension != ".jpg":
            raise CustomError("Extension is not permitted!")

        finalName = generate() +  "-" + createFileDTO.name

        response = self.repository.create(name=finalName,path=createFileDTO.path)

        data = {
            "id": response.id,
            "name": response.name,
            "path": response.path
        }

        return data