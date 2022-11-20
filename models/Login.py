from sqlalchemy import Column, String, Date, ForeignKey, Integer
from database.PostgreSQL import PostgreSQL
from models.User import User


class Login(PostgreSQL.getDB().Base):
    __tablename__ = 'logins'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(64))  # , ForeignKey('users.user_id')
    date_of_login = Column(Date)

    def __init__(self, user_id, date_of_login):
        self.user_id = user_id
        self.date_of_login = date_of_login

    def __str__(self) -> str:
        return str(self.user_id) + " " + str(self.date_of_login)

    def __repr__(self) -> str:
        return str(self)
