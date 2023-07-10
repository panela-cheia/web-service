from database.infra.orm import ORM
from modules.dive.dtos.create_dive_dto import CreateDiveDTO
from modules.dive.dtos.update_dive_dto import UpdateDiveDTO
from database.schema.schema import Dive, User, UsersDive

from sqlalchemy.orm import joinedload

class DiveRepository:
    def __init__(self):
        self.orm = ORM()

    def create(self, data: CreateDiveDTO):
        session = self.orm.get_session()
        
        dive = Dive(
            name=data.name,
            description=data.description,
            photo_id=data.fileId,
            owner_id=data.userId
        )

        session.add(dive)
        session.commit()

        return dive

    def findById(self, id):
        session = self.orm.get_session()
        user = session.query(User).filter_by(id=id).first()

        return user
    
    def findByUsername(self, username):
        session = self.orm.get_session()
        user = session.query(User).filter_by(username=username).first()

        return user

    def findDiveById(self, dive_id):
        session = self.orm.get_session()
        dive = session.query(Dive).filter_by(id=dive_id).options(
            joinedload('owner'),
            joinedload('photo'),
            joinedload('recipe'),
            joinedload('members')
        ).first()

        return dive

    def findDiveByName(self, name):
        session = self.orm.get_session()
        dive = session.query(Dive).filter_by(name=name).first()

        return dive

    def verifyEntry(self, user: str, dive: str) -> bool:
        session = self.orm.get_session()
        values = session.query(UsersDive).filter_by(user_id=user, dive_id=dive).first()

        return values is not None

    def enterDive(self, user_id: str, dive_id: str):
        session = self.orm.get_session()
        user_dive = UsersDive(user_id=user_id, dive_id=dive_id)

        session.add(user_dive)
        session.commit()

        return user_dive

    def exitDive(self, user_id: str, dive_id: str):
        session = self.orm.get_session()
        session.query(UsersDive).filter_by(user_id=user_id, dive_id=dive_id).delete()
        session.commit()

    def update(self, updateDiveDTO: UpdateDiveDTO):
        session = self.orm.get_session()
        dive = session.query(Dive).filter_by(id=updateDiveDTO.id).first()
        dive.description = updateDiveDTO.description
        dive.photo_id = updateDiveDTO.fileId if "fileId" in updateDiveDTO else dive.photo_id
        dive.name = updateDiveDTO.name

        session.commit()

        return dive

    def findAll(self, name: str):
        session = self.orm.get_session()
        dives = session.query(Dive).filter(Dive.name.contains(name)).options(
            joinedload('owner'),
            joinedload('photo'),
            joinedload('recipe'),
            joinedload('members')
        ).all()

        return dives

    def updateDiveOwner(self, dive_id: str, new_owner: str):
        session = self.orm.get_session()
        dive = session.query(Dive).get(dive_id)
        new_owner = session.query(User).get(new_owner)

        if dive and new_owner:
            dive.owner = new_owner
            session.commit()

        return dive

    def findUserDive(self, user_id):
        session = self.orm.get_session()
        dives = session.query(UsersDive).filter_by(user_id=user_id).all()

        return dives
    

    def removeDiveMember(self, user_id: str, dive_id: str):
        session = self.orm.get_session()

        # Verificar se o usuário é membro do mergulho
        users_dive = session.query(UsersDive).filter_by(user_id=user_id, dive_id=dive_id).first()
        if users_dive:
            session.delete(users_dive)
            session.commit()


    def findUserInDive(self, user_id: str, dive_id: str) -> bool:
        session = self.orm.get_session()

        users_dive = session.query(UsersDive).filter_by(user_id=user_id, dive_id=dive_id).first()

        session.close()

        return users_dive is not None

    def getDiveMembersCount(self, dive_id):
        session = self.orm.get_session()
        members_count = session.query(UsersDive).filter_by(dive_id=dive_id).count()

        return members_count
