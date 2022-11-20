from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database(ABC):

    Base = None
    Session = None

    def __init__(self):
        engine = self._connect()
        Database.Session = sessionmaker(bind=engine)
        Database.Base = declarative_base()

    @abstractmethod
    def _connect(self):
        pass

    @staticmethod
    def getDB():
        pass
