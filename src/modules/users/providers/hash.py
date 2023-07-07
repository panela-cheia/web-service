import bcrypt

def hash(value):
    # Generate a salt
    salt = bcrypt.gensalt(rounds=8)
    
    # Hash the value
    hashed_value = bcrypt.hashpw(value.encode('utf-8'), salt)
    
    # Return the hashed value as a string
    return hashed_value.decode('utf-8')

def compare(value,hashed) -> bool:
    return bcrypt.checkpw(value.encode('utf-8'),hashed.encode('utf-8'))