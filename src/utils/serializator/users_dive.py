def usersDiveSerializator(dive):    
    response = {
        "id": dive.dive.id,
        "name":dive.dive.name,
        "description": dive.dive.description,
        "members":str(len([item.user for item in dive.dive.members])) + " membros",
        "recipes": str(len([recipe for recipe in dive.dive.recipe])) + " publicações",
        "photo":{
            "id": dive.dive.photo.id,
            "name":  dive.dive.photo.name,
            "path":  dive.dive.photo.path
        } if dive.dive.photo else None
    }

    return response