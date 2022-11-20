from sqlalchemy import Column, String, Float, Integer
from database.PostgreSQL import PostgreSQL
from models.User import User


class Exchange(PostgreSQL.getDB().Base):
    __tablename__ = 'exchanges'

    currency = Column(String(4),primary_key = True)
    rate = Column(Float)

    def __init__(self, currency, rate):
        self.currency = currency
        self.rate = rate

    def __str__(self) -> str:
        return str(self.currency) + " " + str(self.rate)

    def __repr__(self) -> str:
        return str(self)
