from typing import List
from modules.recipes.dtos.create_recipe_dto import IngredientDTO

def convert_list_to_ingredient_dtos(data: List[dict]) -> List[IngredientDTO]:
    ingredient_dtos = []
    for item in data:
        ingredient_dto = IngredientDTO(name=item['name'], amount=item['amount'], unit=item['unit'])
        ingredient_dtos.append(ingredient_dto)
    return ingredient_dtos