"""Transaction router.

Provides endpoints for creating deposits/withdrawals and listing
transactions for an account.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config import settings
from ..models import DepositAccount, Transaction
from ..api.dependencies import get_db, get_current_user
from ..models.transaction import TransactionCreate, TransactionOut
from ..services.transaction_service import TransactionService

router = APIRouter()

transaction_service = TransactionService()


@router.post("/", response_model=TransactionOut, tags=["transactions"])
async def create_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    tx = transaction_service.create_transaction(db, tx_in, current_user.id)
    return tx


@router.get("/account/{account_id}", response_model=List[TransactionOut], tags=["transactions"])
async def list_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    txs = transaction_service.list_transactions(db, account_id, current_user.id)
    return txs
