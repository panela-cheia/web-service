from database.infra.orm import ORM
from database.schema.schema import File


class FilesRepository:
    def __init__(self):
        self.orm = ORM()

    def create(self, name: str, path: str):
        session = self.orm.get_session()
        
        file = File(
            name=name,
            path=path
        )

        session.add(file)
        session.commit()

        return file

    def delete(self, id):
        session = self.orm.get_session()
        file = session.query(File).filter_by(id=id).first()

        session.delete(file)
        session.commit()

    def findById(self, id):
        session = self.orm.get_session()
        foundedFile = session.query(File).filter_by(id=id).first()

        return foundedFile
    
    def findByName(self, name):
        session = self.orm.get_session()
        foundedFile = session.query(File).filter_by(name=name).first()

        return foundedFile