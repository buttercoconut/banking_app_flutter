from sqlalchemy.orm import Session
from . import models, schemas


def create_deposit(db: Session, deposit: schemas.DepositCreate):
    db_deposit = models.Deposit(**deposit.dict())
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit


def get_deposit(db: Session, deposit_id: int):
    return db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()


def get_deposits(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Deposit).offset(skip).limit(limit).all()
