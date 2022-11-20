from sqlalchemy import Column, String, Date
from database.PostgreSQL import PostgreSQL


class User(PostgreSQL.getDB().Base):
    __tablename__ = 'users'

    user_id = Column(String(64), primary_key=True)
    name = Column(String)
    country = Column(String)
    device = Column(String(32))
    date_of_registration = Column(Date)

    def __init__(self, user_id, name, country, device, date_of_registration):
        self.user_id = user_id
        self.name = name
        self.country = country
        self.device = device
        self.date_of_registration = date_of_registration

    def __str__(self) -> str:
        return str(self.user_id) + " " + str(self.name) + " " + str(self.country) + " " + str(self.device)

    def __repr__(self) -> str:
        return str(self)
