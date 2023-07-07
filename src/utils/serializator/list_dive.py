def listDiveSerializator(dive):
    response = {
        "id": dive.id,
        "name": dive.name,
        "description": dive.description,
        "members": str(len(dive.members)) + " membros",
        "photo": {
            "id": dive.photo.id,
            "name": dive.photo.name,
            "path": dive.photo.path
        } if dive.photo else None,
        "owner_id": dive.owner_id
    }

    return response
