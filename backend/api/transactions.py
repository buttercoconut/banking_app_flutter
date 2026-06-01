"""Transaction router.

Provides endpoints for retrieving transaction history.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.transaction_service import get_transactions
from ..api.dependencies import get_db

router = APIRouter()

@router.get("/{account_id}")
async def list_transactions(account_id: int, db: AsyncSession = Depends(get_db)):
    transactions = await get_transactions(db, account_id)
    return transactions
