from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.schema.schema import Base

from loguru import logger

# Configuração básica do logger
logger.add("app.log", rotation="500 MB", retention="10 days", level="INFO")

class ORM:
    def __init__(self):
        self.engine = create_engine('sqlite:///database/dev.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    def create_tables(self):
        Base.metadata.create_all(self.engine)

        logger.info("Tabelas criadas com sucesso!")

    def get_session(self):
        return self.session