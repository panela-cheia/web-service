class CreateUserDTO:
    def __init__(self,name,username,email,password) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.password = password