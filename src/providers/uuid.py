import uuid

def generate() -> str:
    random_uuid = uuid.uuid4()

    return str(random_uuid)