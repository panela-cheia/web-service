from database.infra.orm import ORM
from database.schema.schema import IngredientsUnit


class IngredientsUnitRepository:
    def __init__(self):
        self.orm = ORM()

    def create(self, name: str):
        session = self.orm.get_session()

        unit = IngredientsUnit(name=name)
        session.add(unit)
        session.commit()

        unit_dict = {
            'id': unit.id,
            'name': unit.name
        }

        session.close()

        return unit_dict

    def delete(self, id):
        session = self.orm.get_session()

        unit = session.query(IngredientsUnit).filter(IngredientsUnit.id == id).first()
        session.delete(unit)
        session.commit()

        session.close()

    def findAll(self):
        session = self.orm.get_session()

        units = session.query(IngredientsUnit).order_by(IngredientsUnit.name).all()

        session.close()

        return units

    def findByName(self, name:str):
        session = self.orm.get_session()

        unit = session.query(IngredientsUnit).filter(IngredientsUnit.name == name).first()

        session.close()

        return unit

    def findById(self, id:str):
        session = self.orm.get_session()

        unit = session.query(IngredientsUnit).filter(IngredientsUnit.id == id).first()

        session.close()

        return unit
