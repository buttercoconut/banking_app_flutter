"""Pydantic schemas for deposit account operations.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, PositiveFloat


class DepositAccountCreate(BaseModel):
    account_number: str = Field(..., min_length=1, max_length=20)
    initial_balance: PositiveFloat = Field(0.0)
    interest_rate: Optional[float] = Field(0.01, ge=0.0, le=1.0)


class DepositAccountOut(BaseModel):
    id: int
    account_number: str
    balance: float
    interest_rate: float
    last_interest_applied: str
    customer_id: int

    class Config:
        orm_mode = True
