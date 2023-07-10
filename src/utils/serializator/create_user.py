def createUserSerializator(user):
    response = {
        "id":user["id"],
        "name":user["name"],
        "username":user["username"],
        "email":user["email"]
    }

    return response