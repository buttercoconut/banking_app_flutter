from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DepositBase(BaseModel):
    account_number: str = Field(..., example="1234567890")
    amount: float = Field(..., gt=0, example=1000.00)
    currency: str = Field("USD", max_length=3, example="USD")

class DepositCreate(DepositBase):
    pass

class Deposit(DepositBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
