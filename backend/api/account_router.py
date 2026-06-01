"""Account management router.

Endpoints for creating accounts, retrieving account details and
applying interest.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import settings
from ..models import DepositAccount, Customer, Transaction
from ..api.dependencies import get_db, get_current_user
from ..models.deposit_account import DepositAccountCreate, DepositAccountOut
from ..services.account_service import AccountService

router = APIRouter()

account_service = AccountService()


@router.post("/", response_model=DepositAccountOut, tags=["accounts"])
async def create_account(
    account_in: DepositAccountCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    account = account_service.create_account(db, current_user.id, account_in)
    return account


@router.get("/", response_model=List[DepositAccountOut], tags=["accounts"])
async def list_accounts(
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    accounts = db.query(DepositAccount).filter(DepositAccount.customer_id == current_user.id).all()
    return accounts


@router.get("/{account_id}", response_model=DepositAccountOut, tags=["accounts"])
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    account = db.query(DepositAccount).filter(DepositAccount.id == account_id).first()
    if not account or account.customer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/{account_id}/interest", response_model=DepositAccountOut, tags=["accounts"])
async def apply_interest(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    account = account_service.apply_interest(db, account_id, current_user.id)
    return account
