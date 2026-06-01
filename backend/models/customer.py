"""Pydantic schemas for request/response validation.

These schemas are used by the API layer to validate incoming data and
to shape outgoing JSON responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveFloat


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class DepositAccountCreate(BaseModel):
    account_number: str = Field(..., min_length=1, max_length=20)
    initial_balance: PositiveFloat = Field(0.0)
    interest_rate: Optional[float] = Field(0.01, ge=0.0, le=1.0)


class DepositAccountOut(BaseModel):
    id: int
    account_number: str
    balance: float
    interest_rate: float
    last_interest_applied: datetime
    customer_id: int

    class Config:
        orm_mode = True


class TransactionCreate(BaseModel):
    account_id: int
    amount: PositiveFloat
    type: str = Field(..., regex="^(deposit|withdrawal|interest)$")


class TransactionOut(BaseModel):
    id: int
    account_id: int
    amount: float
    type: str
    timestamp: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
