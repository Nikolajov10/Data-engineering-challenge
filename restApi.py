from models.User import User
from datetime import date
from database.PostgreSQL import PostgreSQL
from models.User import User
from models.Login import Login
from models.Exchange import Exchange
from models.Transaction import Transaction
from sqlalchemy import and_
from sqlalchemy import func as f

def getExchange(session) ->dict:
    exchange = dict()
    exchange["EUR"] = session.query(Exchange).filter(Exchange.currency == "EUR").first().rate
    exchange["USD"] = session.query(Exchange).filter(Exchange.currency == "USD").first().rate
    return exchange

def transactionsStats(trans, exchange, byCountry=False):
    numberOfTrans = 0
    revenue = 0
    countriesStats = dict()
    for tr in trans:
        if not byCountry:
            revenue += tr.trans_amount * exchange[tr.trans_currency]
            numberOfTrans += 1
        else:
            countryStats = countriesStats.get(tr.country, [0, 0])
            countryStats[0] += tr.trans_amount * exchange[tr.trans_currency]
            countryStats[1] += 1
            countriesStats[tr.country] = countryStats
    if byCountry:
        return countriesStats, None
    return revenue, numberOfTrans


def userStats(user_id, _date: date = None):
    db = PostgreSQL.getDB()
    db.Base.metadata.create_all(db.engine)
    session = db.Session()
    user = session.query(User).filter(
        User.user_id == user_id).first()
    if not user:
        return None
    country = user.country
    name = user.name
    numberOfLogins = 0
    numberOfTrans = 0
    trans = []
    revenue = 0.0
    if _date:
        numberOfLogins = session.query(Login).filter(
            and_(Login.user_id == user_id, Login.date_of_login == _date)
        ).count()
        trans = session.query(Transaction).filter(
            and_(Transaction.user_id == user_id,
                 Transaction.date_of_trans == _date)
        ).all()
    else:
        numberOfLogins = session.query(Login).filter(
            Login.user_id == user_id
        ).count()
        trans = session.query(Transaction).filter(
            Transaction.user_id == user_id).all()

    exchange = getExchange(session)

    revenue, numberOfTrans = transactionsStats(trans, exchange)

    userLastlog = session.query(Login).filter(
        Login.user_id == user_id
    ).order_by(Login.date_of_login.desc()).first()
    dateBenchmark = _date if _date else session.query(Login).order_by(
        Login.date_of_login.desc()).first().date_of_login
    daysPassed = abs((dateBenchmark - userLastlog.date_of_login).days)

    ret = dict()
    ret['country'] = country
    ret['name'] = name
    ret['numberOfLogins'] = numberOfLogins
    ret['numberOfTrans'] = numberOfTrans
    ret['revenue'] = revenue
    ret['daysPassed'] = daysPassed
    return ret


def gameStats(_date: date = None, country = None):
    db = PostgreSQL.getDB()
    db.Base.metadata.create_all(db.engine)
    session = db.Session()
    numberOfLogins = 0
    activeUsers = 0
    if _date:
        if not country:
            activeUsers = session.query(Login).distinct(Login.user_id).filter(
                Login.date_of_login == _date).count()
            numberOfLogins = session.query(Login).filter(
                Login.date_of_login == _date).count()
            trans = session.query(Transaction).filter(
                Transaction.date_of_trans == _date).all()
        else:
            activeUsers = session.query(f.count(f.distinct(Login.user_id)), User.country).filter(
                Login.date_of_login == _date, Login.user_id == User.user_id).group_by(User.country).all()

            numberOfLogins = session.query(f.count(Login.user_id), User.country).filter(
                Login.date_of_login == _date, Login.user_id == User.user_id).group_by(User.country).all()

            trans = session.query(Transaction.trans_amount, Transaction.trans_currency, User.country).filter(
                Transaction.date_of_trans == _date, Transaction.user_id == User.user_id).all()
    else:
        if not country:
            activeUsers = session.query(Login).distinct(Login.user_id).count()
            numberOfLogins = session.query(Login).filter().count()
            trans = session.query(Transaction).filter().all()
        else:
            activeUsers = session.query(f.count(f.distinct(Login.user_id)), User.country).filter(
                Login.user_id == User.user_id).group_by(User.country).all()

            numberOfLogins = session.query(f.count(Login.user_id), User.country).filter(
                Login.user_id == User.user_id).group_by(User.country).all()

            trans = session.query(Transaction.trans_amount, Transaction.trans_currency, User.country).filter(
                Transaction.user_id == User.user_id).all()

    exchange = getExchange(session)
    revenue, numberOfTrans = transactionsStats(
        trans, exchange, country != None)

    ret = dict()

    if not country:

        ret['activeUsers'] = activeUsers
        ret['numberOfLogins'] = numberOfLogins
        ret['numberOfTrans'] = numberOfTrans
        ret['revenue'] = revenue

    else:
        ret['activeUsers'] = dict()
        ret['numberOfLogins'] = dict()
        ret['numberOfTrans'] = dict()
        ret['revenue'] = dict()
        for stats in activeUsers:
            ret['activeUsers'][stats[1]] = stats[0]
        for stats in numberOfLogins:
            ret['numberOfLogins'][stats[1]] = stats[0]
        for key in revenue:
            ret['numberOfTrans'][key] = revenue[key][0]
            ret['revenue'][key] = revenue[key][1]
    return ret
