from modules.recipes.repositories.recipe_repository import RecipeRepository
from modules.recipes.dtos.reactions_dto import ReactionDTO

class ReactionRecipeUseCase:
    def __init__(self,repository:RecipeRepository) -> None:
        self.repository = repository
    
    def execute(self, reaction_data: ReactionDTO) -> None:
        try:
            recipe_id = reaction_data.recipe_id
            user_id = reaction_data.user_id

            # Verificar se o usuário já reagiu à receita anteriormente
            existing_reaction = self.repository.verify_existing_reaction(recipe_id=recipe_id,user_id=user_id)

            if existing_reaction:
                # Atualizar a reação existente
                self.repository.updateReaction(id=existing_reaction.id,type=reaction_data.type)
            else:
                # Criar uma nova reação
                self.repository.reaction(
                    type=reaction_data.type,
                    recipe_id=recipe_id,
                    user_id=user_id
                )
            return {"ok": "successufully reacted!"}
        except (ValueError):
            return {"error": ValueError}