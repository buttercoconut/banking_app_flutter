"""Custom validators for the banking backend.

These validators are used by Pydantic models to enforce business rules
such as positive amounts and valid interest rates.
"""

from __future__ import annotations

from pydantic import validator

from .deposit_account import DepositAccountCreate

class DepositAccountCreateWithValidation(DepositAccountCreate):
    @validator("interest_rate")
    def rate_between_0_and_1(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError("interest_rate must be between 0 and 1")
        return v

    @validator("initial_balance")
    def balance_non_negative(cls, v):
        if v < 0:
            raise ValueError("initial_balance must be non‑negative")
        return v
