from modules.dive.repositories.dive_repository import DiveRepository
from modules.dive.dtos.exit_dive_dto import ExitDiveDTO

class ExitDiveUseCase:
    def __init__(self, repository: DiveRepository) -> None:
        self.repository = repository
    
    def execute(self, data:ExitDiveDTO):
        try:
            
            # Verificar se o buteco a ser deixado existe
            exit_dive = self.repository.findDiveById(data.diveId)

            print(exit_dive)
            if not exit_dive:
                return { "error":"Dive does not exist" }
            
            # Verificar se o usuário existe
            user = self.repository.findById(id=data.user)
            if not user:
                return { "error":"User does not exist" }
    
            # o usuario é owner
            if exit_dive.owner.id == data.user and data.new_owner:
                
                # Verificar se o usuário existe
                verify_new_owner_user = self.repository.findByUsername(username=data.new_owner)
                if not verify_new_owner_user:
                    return { "error":"New Owner user does not exist" }

                # Verificar se o usuário que está saindo é um membro do dive
                is_member = self.repository.findUserInDive(dive_id=data.diveId,user_id=verify_new_owner_user.id)
                if is_member:
                    # Remover o usuário como membro do dive
                    self.repository.removeDiveMember(data.user, data.diveId)

                    # atualiza o owner como new_owner
                    self.repository.updateDiveOwner(data.diveId,verify_new_owner_user.id)

                    response = { "ok": "Successfully left the dive and this dive has a new owner!" }
                else:
                    response = { "error": "To owner left the dive is required to be in the dive" }

            elif exit_dive.owner.id == data.user and not data.new_owner:
                response = { "error": "To owner left the dive is required new owner!" }

            # usuario comum!
            else:
                # Verificar se o usuário que está saindo é um membro do dive
                is_member = self.repository.findUserInDive(dive_id=data.diveId,user_id=data.user)
                if is_member:
                    # Remover o usuário como membro do dive
                    self.repository.removeDiveMember(data.user, data.diveId)

                    response = { "ok": "Successfully left the dive!" }
            
            return response

        except ( ValueError):
            response = { "error": ValueError }