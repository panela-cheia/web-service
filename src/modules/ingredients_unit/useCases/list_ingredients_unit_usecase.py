from modules.ingredients_unit.repositories.ingredients_unit_repository import IngredientsUnitRepository

from utils.serializator.ingredients_unit import ingredientsUnitSerializator

class ListIngredientsUnitUseCase:
    def __init__(self, repository: IngredientsUnitRepository) -> None:
        self.repository = repository

    def execute(self):
        try:
            units = self.repository.findAll()

            data = []

            for unit in units:

                data.append(ingredientsUnitSerializator(
                    ingredientsUnit={"id": unit.id, "name": unit.name}))

            return data
        except (ValueError):
            return {"error": ValueError}
