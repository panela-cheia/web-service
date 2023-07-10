import pytz

timezone = pytz.timezone('America/Sao_Paulo')


def format_datetime(dt):
    if dt:
        localized_dt = dt.astimezone(timezone)
        return localized_dt.strftime("%d/%m/%Y")
    return None


def serialize_user(user):
    user_dict = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'barn': {
            "user_id": user.barn[0].__dict__["user_id"],
            "id": user.barn[0].__dict__["id"]
        },
        'followers': [{'following_id': follower.following_id, 'follower_id': follower.follower_id} for follower in user.followers],
        'following': [{'following_id': following.following_id, 'follower_id': following.follower_id} for following in user.following],
        'owners_dive': [owner_dive.__dict__ for owner_dive in user.owners_dive],
        'photo': user.photo.__dict__ if user.photo else None,
        'reactions': [reaction.__dict__ for reaction in user.reactions],
        'recipes': [
            {
                'name': recipe.name,
                'description': recipe.description,
                'barn_id': recipe.barn_id,
                'photo_id': recipe.photo_id,
                'updated_at': format_datetime(recipe.updated_at),
                'id': recipe.id,
                'user_id': recipe.user_id,
                'dive_id': recipe.dive_id,
                'created_at': format_datetime(recipe.created_at)
            } for recipe in user.recipes],
        'users_dive': [user_dive.__dict__ for user_dive in user.users_dive]
    }
    return user_dict
