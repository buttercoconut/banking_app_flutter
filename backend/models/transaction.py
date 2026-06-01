"""Pydantic schemas for transaction operations.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, PositiveFloat


class TransactionCreate(BaseModel):
    account_id: int
    amount: PositiveFloat
    type: str = Field(..., regex="^(deposit|withdrawal|interest)$")


class TransactionOut(BaseModel):
    id: int
    account_id: int
    amount: float
    type: str
    timestamp: str

    class Config:
        orm_mode = True
