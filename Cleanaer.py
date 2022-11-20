from FileDataParser import FileDataParser
from enum import Enum
from datetime import datetime as dt
from database.PostgreSQL import PostgreSQL
from models.User import User
from models.Login import Login
from models.Transaction import Transaction
from models.Exchange import Exchange

class EventType(Enum):
    Login = "login"
    Register = "registration"
    Transaction = "transaction"


class Cleaner:

    def __init__(self, parser: FileDataParser) -> None:
        self.__parser = parser

    @staticmethod
    def cleanName(name):
        # check if there is . in name and return only name part
        if not name:
            return None
        parts = name.split(" ")
        cleanedName = ""
        for part in parts:
            bad = False
            for letter in part:
                if not letter.isalpha() and letter != "-":
                    bad = True
                    break
            if not bad:
                if cleanedName != "":
                    cleanedName += " "
                cleanedName += part
        return cleanedName

    def cleanAndStoreData(self) -> None:
        data = self.__parser.parseData()
        events = set()
        db = PostgreSQL.getDB()
        db.Base.metadata.create_all(db.engine)
        session = db.Session()
        possibleAmounts = set([0.99, 1.99, 2.99, 4.99, 9.99])
        possibleCurrency = set(["USD", "EUR"])
        possilbeDevices = set(["Android", "Web", "iOS"])
        for event in data:
            eventId = event.get('event_id', None)
            eventData = event.get('event_data', None)
            if eventId in events or not eventId or not eventData:
                # duplicate event
                continue
            badData = False
            eventType = event.get('event_type', None)
            date = event.get('event_timestamp', None)
            if not date:
                continue
            date = dt.fromtimestamp(int(date)).date()
            if eventType == EventType.Register.value:
                country = eventData.get('country', None)
                name = Cleaner.cleanName(eventData.get('name', None))
                userId = eventData.get('user_id', None)
                device = eventData.get('device_os', None)
                if device not in possilbeDevices or not userId or not country or not name or len(country) > 3:
                    continue
                user = User(userId, name, country,  device, date)
                try:
                    session.add(user)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    badData = True

            elif eventType == EventType.Login.value:
                userId = eventData.get('user_id', None)
                if not userId:
                    continue
                login = Login(userId, date)
                try:
                    session.add(login)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    badData = True

            elif eventType == EventType.Transaction.value:
                userId = eventData.get('user_id', None)
                if not userId:
                    continue
                transCurr = eventData.get('transaction_currency', None)
                transAmount = eventData.get('transaction_amount', None)
                if transCurr not in possibleCurrency or transAmount not in possibleAmounts:
                    continue
                trans = Transaction(userId, transCurr, transAmount, date)
                try:
                    session.add(trans)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    badData = True
            else:
                badData = True
            if not badData:
                events.add(eventId)
        session.close()

    def setParser(self, parser) -> None:
        self.__parser = parser

    def getParser(self) -> FileDataParser:
        return self.__parser

    def getExchangeRate(self, file):
        self.__parser.setFilePath(file)
        data = self.__parser.parseData()
        rates = dict()
        db = PostgreSQL.getDB()
        db.Base.metadata.create_all(db.engine)
        session = db.Session()
        for d in data:
            curr = d.get('currency',None)
            rate = float(d.get('rate_to_usd',-1))
            if not curr or rate < 0:
                continue
            ex = Exchange(curr,rate)
            try:
                session.add(ex)
                session.commit()
            except Exception as e:
                session.rollback()
        session.close()

