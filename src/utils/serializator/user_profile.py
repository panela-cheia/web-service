from utils.serializator.recipe_without_reactions import recipeWithoutReactionsSerializator

def userProfileSerializator(user):
    
    recipes = []

    for recipe in user.recipes:
        recipes.append(recipeWithoutReactionsSerializator(recipe=recipe))

    data = {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "bio": user.bio,
        "photo": {
            "id": user.photo.id,
            "name": user.photo.name,
            "path": user.photo.path
        } if user.photo else None,
        "posts": str(len(user.recipes)),
        "following":str(len(user.following)),
        "followers":str(len(user.followers)),
        "recipes":recipes
    }

    return data