from modules.ingredients_unit.repositories.ingredients_unit_repository import IngredientsUnitRepository

from utils.serializator.ingredients_unit import ingredientsUnitSerializator

class CreateIngredientsUnitUseCase:
    def __init__(self,repository:IngredientsUnitRepository) -> None:
        self.repository = repository

    def execute(self,name:str):
        try:
            verifyIfUnitAlreadyBeenRegistered = self.repository.findByName(name=name)

            if verifyIfUnitAlreadyBeenRegistered:
                return { "error":"This name already been registered!" }

            unit =  self.repository.create(name=name)

            return ingredientsUnitSerializator(ingredientsUnit=unit)
        except (ValueError):
            return { "error":ValueError }