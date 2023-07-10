from modules.dive.repositories.dive_repository import DiveRepository

class EnterDiveUseCase:
    def __init__(self, repository: DiveRepository) -> None:
        self.repository = repository
    
    def execute(self, user_id: str, dive_id: str):
        
        # Verificar se o usuário existe
        user = self.repository.findById(id=user_id)
        if not user:
            return {"error":"User does not exist"}
        
        # Verificar se o buteco a ser entrado existe
        enter_dive = self.repository.findDiveById(dive_id)
        if not enter_dive:
            raise {"error":"Dive does not exist"}
        
        # Verificar se o usuário está tentando entrar em um buteco que ele já está inserido
        existing_dive = self.repository.verifyEntry(user=user_id, dive=dive_id)

        if existing_dive:
            raise {"error":"Already in this dive"}
        

        # Criar o relacionamento
        self.repository.enterDive(user_id, dive_id)

        data = {"ok": "Successfully joined the dive"}

        return data