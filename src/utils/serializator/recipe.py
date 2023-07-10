import pytz
from modules.users.repositories.user_repository import UserRepository as repo

timezone = pytz.timezone('America/Sao_Paulo')

def recipeSerializator(recipe, reactions):
    repository = repo()
    user= repository.findById(recipe.user_id)

    recipe_formatted = {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "user": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "photo": {
                "id": recipe.user.photo.id,
                "name": recipe.user.photo.name,
                "path": recipe.user.photo.path
            } if recipe.user.photo else None
        },
        "dive":{
            "id": recipe.dive.id,
            "name": recipe.dive.name,
        } if recipe.dive else None,
        "photo": {
            "id": recipe.photo.id,
            "name": recipe.photo.name,
            "path": recipe.photo.path
        } if recipe.photo else None,
        "ingredients":[{
            "name": ingredient.name,
            "amount": ingredient.amount,
            "unit": ingredient.unit
        } for ingredient in recipe.ingredients],
        "reactions": {
            "bao": str(reactions["bão"]),
            "mio_de_bao": str(reactions["mió de bão"]),
            "agua_na_boca": str(reactions["água na boca"])
        },
        "created_at": recipe.created_at.astimezone(timezone).strftime("%d/%m/%Y")
    }

    return recipe_formatted