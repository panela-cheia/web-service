from modules.barn.repositories.barn_repository import BarnRepository
from modules.users.repositories.user_repository import UserRepository

from utils.serializator.recipe_without_reactions import recipeWithoutReactionsSerializator

class UsersBarnUseCase:
    def __init__(self,userRepository:UserRepository, barnRepository:BarnRepository) -> None:
        self.userRepository = userRepository
        self.barnRepository = barnRepository

    def execute(self,user_id:str):
        user = self.userRepository.findById(id=user_id)

        barn =  self.barnRepository.findAll(barnId=user.barn[0].id)

        if barn is None:
            return []
        
        recipes = []

        for recipe in barn.recipes:
            recipes.append(recipeWithoutReactionsSerializator(recipe=recipe))
        
        return recipes