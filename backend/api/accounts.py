"""Account router.

Provides endpoints for account operations such as creating an account,
depositing, withdrawing and calculating interest.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.account_service import create_account, deposit, withdraw, calculate_interest
from ..api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=DepositAccountOut)
async def create_account_endpoint(customer_id: int, db: AsyncSession = Depends(get_db)):
    # Create a new deposit account for the customer
    new_account = await create_account(db, customer_id)
    return DepositAccountOut.from_orm(new_account)

@router.post("/{account_id}/deposit", response_model=DepositAccountOut)
async def deposit_endpoint(account_id: int, amount: float, db: AsyncSession = Depends(get_db)):
    # Perform deposit operation
    account = await get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.balance += amount
    await db.commit()
    return DepositAccountOut.from_orm(account)

@router.post("/{account_id}/withdraw", response_model=DepositAccountOut)
async def withdraw_endpoint(account_id: int, amount: float, db: AsyncSession = Depends(get_db)):
    account = await get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    account.balance -= amount
    await db.commit()
    return DepositAccountOut.from_orm(account)

@router.get("/{account_id}/interest", response_model=DepositAccountOut)
async def calculate_interest_endpoint(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    interest = await calculate_interest(db, account_id)
    return DepositAccountOut.from_orm(account)
