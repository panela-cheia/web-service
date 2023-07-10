import json
import Pyro5.server
from constants.topics import Topics
from loguru import logger

# repositories
from modules.recipes.repositories.recipe_repository import RecipeRepository

# useCase
from modules.recipes.useCases.reaction_recipe_usecase import ReactionRecipeUseCase, ReactionDTO

from modules.recipes.dtos.reactions_dto import ReactionType

@Pyro5.server.expose
class ReactionRecipeAdapter(object):
    def __init__(self) -> None:
        self.useCase = ReactionRecipeUseCase(repository=RecipeRepository())

    def execute(self,type:str,recipe_id:str,user_id:str):
        typeR = ReactionType(type)
        dto = ReactionDTO(
            type=typeR.value,
            recipe_id=recipe_id,
            user_id=user_id
        )
        
        recipe = self.useCase.execute(reaction_data=dto)
        
        if "error" in recipe:
            logger.error("{topic} - {response}",topic=Topics.RECIPE_REACTION.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))
        else:
            logger.info("{topic} - {response}",topic=Topics.RECIPE_REACTION.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))

        return recipe