from modules.dive.repositories.dive_repository import DiveRepository
from utils.serializator.list_dive import listDiveSerializator

class SearchDiveUseCase:
    def __init__(self, repository: DiveRepository):
        self.repository = repository

    def execute(self, diveName: str):
        dives =  self.repository.findAll(name=diveName)

        all_dives = []

        for dive in dives:
            dive_formatted = listDiveSerializator(dive=dive)
            all_dives.append(dive_formatted)

        return all_dives