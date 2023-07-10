import pytz

timezone = pytz.timezone('America/Sao_Paulo')

def recipeWithoutReactionsSerializator(recipe):
    recipe_formatted = {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "photo": {
            "id": recipe.photo.id ,
            "name": recipe.photo.name,
            "path": recipe.photo.path
        } if recipe.photo else None,
        "ingredients": [{
            "name": ingredient.name,
            "amount": ingredient.amount,
            "unit": ingredient.unit
        } for ingredient in recipe.ingredients],
        "created_at": recipe.created_at.astimezone(timezone).strftime("%d/%m/%Y")
    }

    return  recipe_formatted
