from database.Database import Database
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


class PostgreSQL(Database):

    db = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def getDB():
        if not PostgreSQL.db:
            PostgreSQL.db = PostgreSQL()
        return PostgreSQL.db

    def _connect(self):
        load_dotenv()
        self.engine = create_engine(
            f"postgresql://{os.getenv('POSTGRE_USER')}:{os.getenv('POSTGRE_PASSWORD')}@localhost:{os.getenv('POSTGRE_PORT')}/{os.getenv('POSTGRE_DB')}"
        )
        return self.engine


db = PostgreSQL()
