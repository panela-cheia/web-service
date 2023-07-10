def searchUsersSerializator(user):

    user_dict = user["user"].__dict__

    result = {
        "id": user_dict["id"],
        "name": user_dict["name"],
        "username": user_dict["username"],
        "photo": {
            "id": user_dict["photo"].id,
            "name": user_dict["photo"].name,
            "path": user_dict["photo"].path
        } if user_dict["photo"] else None,
        "common_followers": str(user["common_followers"]) + " amigo(s)",
        "common_dives": str(user["common_dives"]) + " buteco(s)"
    }

    return result