from sqlalchemy.orm import joinedload

from database.schema.schema import Barn, Recipe
from database.infra.orm import ORM

from modules.barn.dtos.save_recipe_dto import BarnSaveRecipeDTO
from modules.barn.dtos.remove_recipe_dto import RemoveRecipeDTO


class BarnRepository:
    def __init__(self):
        self.orm = ORM()

    def save(self, data: BarnSaveRecipeDTO):
        session = self.orm.get_session()

        barn = session.query(Barn).filter_by(id=data.barnId).first()
        recipe = session.query(Recipe).filter_by(id=data.recipeId).first()

        barn.recipes.append(recipe)
        session.commit()

        return barn

    def findAll(self, barnId: str):
        session = self.orm.get_session()
        barn = session.query(Barn).filter_by(id=barnId).options(
            joinedload('recipes').joinedload('ingredients'),
            joinedload('recipes').joinedload('photo')
        ).first()

        if barn:
            return barn
        else:
            return None

    def removeRecipe(self, data: RemoveRecipeDTO):
        session = self.orm.get_session()

        barn = session.query(Barn).filter_by(id=data.barnId).first()
        recipe = session.query(Recipe).filter_by(id=data.recipeId).first()

        barn.recipes.remove(recipe)
        session.commit()

        return barn