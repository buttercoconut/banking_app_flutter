"""Customer router.

Provides CRUD operations for customers.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.dependencies import get_db
from ..models.deposit_account import Customer, CustomerCreate, CustomerOut
from ..services.account_service import create_account

router = APIRouter()

@router.post("/", response_model=CustomerOut)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return CustomerOut.from_orm(new_customer)

@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerOut.from_orm(customer)

@router.post("/{customer_id}/accounts", response_model=CustomerOut)
async def create_customer_account(customer_id: int, db: AsyncSession = Depends(get_db)):
    # Create a new deposit account for the customer
    await create_account(db, customer_id)
    # Return updated customer with accounts
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one()
    return CustomerOut.from_orm(customer)
