from modules.files.repositories.files_repository import FilesRepository
from modules.files.dtos.delete_file_dto import DeleteFileDTO

#from shared.errors.errors import CustomError

class DeleteFileUseCase:
    def __init__(self, repository: FilesRepository) -> None:
        self.repository = repository

    def execute(self, deleteFileDTO:DeleteFileDTO):

        verifyIfFileExists = self.repository.findById(id=deleteFileDTO.id)

        if not verifyIfFileExists:
            
            return { "error":"File not found" }
        
        try:
            self.repository.delete(deleteFileDTO.id)
            return { "ok":"Successfully delete file" }
        except:
            raise { "error":"An error occurred during file deletion" }
