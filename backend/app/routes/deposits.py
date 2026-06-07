from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Deposit, status_code=status.HTTP_201_CREATED)
def create_deposit(deposit: schemas.DepositCreate, db: Session = Depends(database.get_db)):
    return crud.create_deposit(db, deposit)

@router.get("/{deposit_id}", response_model=schemas.Deposit)
def read_deposit(deposit_id: int, db: Session = Depends(database.get_db)):
    db_deposit = crud.get_deposit(db, deposit_id)
    if db_deposit is None:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return db_deposit

@router.get("/", response_model=List[schemas.Deposit])
def read_deposits(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    deposits = crud.get_deposits(db, skip=skip, limit=limit)
    return deposits
