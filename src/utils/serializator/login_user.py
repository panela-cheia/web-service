def loginUserSerializator(user,token):
    response = {
        "user":{
            "id":user.id,
            "name":user.name,
            "username":user.username,
            "bio":user.bio,
            "email":user.email,
            "barnId": user.barn[0].id,
            "photo": {
                "id": user.photo.id,
                "name": user.photo.name,
                "path": user.photo.path
            } if user.photo else None
        },
        "token":token.decode('utf-8')
    }

    return response