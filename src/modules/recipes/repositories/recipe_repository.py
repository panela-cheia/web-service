from database.schema.schema import Recipe, Ingredients, Reaction
from database.infra.orm import ORM

from src.modules.recipes.dtos.create_recipe_dto import CreateRecipeDTO

from sqlalchemy.orm import joinedload

class RecipeRepository:
    def __init__(self):
        self.orm = ORM()
    
    def create(self, data: CreateRecipeDTO):
        session = self.orm.get_session()
        
        recipe = Recipe(
            name=data.name,
            description=data.description,
            user_id=data.userId,
            dive_id=data.diveId,
            photo_id=data.fileId
        )

        ingredients = [
            Ingredients(name=ingredient.name, amount=ingredient.amount, unit=ingredient.unit)
            for ingredient in data.ingredients
        ]
        recipe.ingredients = ingredients

        session.add(recipe)
        session.commit()
        session.refresh(recipe)

        return recipe

    def findAll(self):
        session = self.orm.get_session()
        
        recipes = session.query(Recipe).\
            options(joinedload(Recipe.barn), joinedload(Recipe.dive),
                    joinedload(Recipe.ingredients), joinedload(Recipe.photo),
                    joinedload(Recipe.reactions), joinedload(Recipe.user)).\
            order_by(Recipe.created_at.desc()).all()

        return recipes

    def search(self, name: str):
        session = self.orm.get_session()
        
        recipes = session.query(Recipe).\
            options(joinedload(Recipe.barn), joinedload(Recipe.dive),
                    joinedload(Recipe.ingredients), joinedload(Recipe.photo),
                    joinedload(Recipe.reactions), joinedload(Recipe.user)).\
            filter(Recipe.name.ilike(f'%{name}%')).all()

        return recipes

    def verify_existing_reaction(self, recipe_id: str, user_id: str):
        session = self.orm.get_session()
        
        existing_reaction = session.query(Reaction).\
            filter(Reaction.recipe_id == recipe_id, Reaction.user_id == user_id).first()

        return existing_reaction

    def reaction(self, recipe_id: str, type: str, user_id: str):
        session = self.orm.get_session()
        reaction = Reaction(type=type, recipe_id=recipe_id, user_id=user_id)

        session.add(reaction)
        session.commit()
        session.refresh(reaction)

        return reaction

    def updateReaction(self, id: int, type: str):
        session = self.orm.get_session()
        reaction = session.query(Reaction).get(id)

        if reaction:
            reaction.type = type
            session.commit()
            return reaction
        else:
            return None

    def getReactionQuantities(self, recipe_id: str):
        session = self.orm.get_session()
        
        reaction_quantities = {
            "bão": 0,
            "mió de bão": 0,
            "água na boca": 0
        }

        try:
            recipe_reactions = session.query(Reaction).filter(Reaction.recipe_id == recipe_id).all()

            for reaction in recipe_reactions:
                if reaction.type in reaction_quantities:
                    reaction_quantities[reaction.type] += 1
        except Exception as e:
            # Lidar com exceção de consulta
            print(e)

        return reaction_quantities
