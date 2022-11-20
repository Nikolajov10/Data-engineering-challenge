from sqlalchemy import Column, String, Date, ForeignKey, Float, Integer
from database.PostgreSQL import PostgreSQL


class Transaction(PostgreSQL.getDB().Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(64))  # ForeignKey('users.user_id')
    trans_currency = Column(String(8))
    trans_amount = Column(Float)
    date_of_trans = Column(Date)

    def __init__(self, user_id, trans_currency, trans_amount, date_of_trans):
        self.user_id = user_id
        self.trans_currency = trans_currency
        self.trans_amount = trans_amount
        self.date_of_trans = date_of_trans

    def __str__(self) -> str:
        return str(self.user_id) + " " + str(self.trans_amount) + " " + str(self.trans_currency)

    def __repr__(self) -> str:
        return str(self)
