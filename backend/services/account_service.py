"""Service layer for account operations.

Handles business logic such as creating accounts and applying interest.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from ..models import DepositAccount, Customer, Transaction
from ..models.deposit_account import DepositAccountCreate

class AccountService:
    def create_account(self, db: Session, customer_id: int, account_in: DepositAccountCreate) -> DepositAccount:
        # Ensure account number uniqueness
        if db.query(DepositAccount).filter(DepositAccount.account_number == account_in.account_number).first():
            raise ValueError("Account number already exists")
        account = DepositAccount(
            account_number=account_in.account_number,
            balance=account_in.initial_balance,
            interest_rate=account_in.interest_rate,
            customer_id=customer_id,
            last_interest_applied=datetime.utcnow(),
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def apply_interest(self, db: Session, account_id: int, customer_id: int) -> DepositAccount:
        account = db.query(DepositAccount).filter(DepositAccount.id == account_id).first()
        if not account or account.customer_id != customer_id:
            raise ValueError("Account not found or access denied")
        # Simple annual interest calculation
        days_since = (datetime.utcnow() - account.last_interest_applied).days
        if days_since <= 0:
            return account
        interest = account.balance * account.interest_rate * (days_since / 365)
        account.balance += interest
        account.last_interest_applied = datetime.utcnow()
        # Record transaction
        tx = Transaction(account_id=account.id, amount=interest, type="interest")
        db.add(tx)
        db.commit()
        db.refresh(account)
        return account
