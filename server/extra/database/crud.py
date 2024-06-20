from sqlalchemy import and_, update
from sqlalchemy.orm import Session

import database.models as models
import database.schemas as schemas


def get_user_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def bet_result(db: Session, id: int):
    return db.query(models.Bet).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, name: str):
    db_user = models.User(name=name, balance = 100.0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def check_if_user_has_open_bet(db: Session, user_id: int, table_id: int):
    bet = db.query(models.Bet) \
        .filter(models.Bet.completed == False) \
        .filter(models.Bet.user_id == user_id) \
        .filter(models.Bet.table_id == table_id) \
        .first()

    return bet if bet else False

def create_bet(db: Session, user_id: int, table_id: int, type: str, value: str, amount: float):
    db_bet = models.Bet(user_id=user_id, table_id=table_id, type=type, value=value, amount=amount)
    db.add(db_bet)
    db.commit()
    db.refresh(db_bet)
    return db_bet

def create_table(db: Session):
    db_table = models.RouletteTable()
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def process_bet(db: Session, bet_id, user_id, table_id, earnings: int):
    try:
        user = db.query(models.User).get(user_id)
        bet = db.query(models.Bet).get(bet_id)
    except Exception as e:
        return

    db_balance_history = models.BalanceUpdate(
        table_id=table_id,
        user_id=user_id,
        bet_id=bet_id,
        bet_earnings=earnings,
    )

    user.balance += earnings
    bet.completed = True

    db.add(db_balance_history)
    db.commit()

def get_tables(db: Session):
    tables = db.query(models.RouletteTable)

    for table in tables:
        yield table

def close_all_open_bets(db: Session):
    stmt = (
        update(models.Bet).
        where(models.Bet.completed == False).
        values(completed = True)
    )
    db.execute(statement=stmt)
    db.commit()


