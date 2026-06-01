"""Service layer for transaction operations.

Handles deposits, withdrawals and transaction listing.
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from ..models import DepositAccount, Transaction
from ..models.transaction import TransactionCreate

class TransactionService:
    def create_transaction(self, db: Session, tx_in: TransactionCreate, customer_id: int) -> Transaction:
        account = db.query(DepositAccount).filter(DepositAccount.id == tx_in.account_id).first()
        if not account or account.customer_id != customer_id:
            raise ValueError("Account not found or access denied")
        if tx_in.type == "withdrawal" and account.balance < tx_in.amount:
            raise ValueError("Insufficient funds")
        # Update balance
        if tx_in.type == "deposit":
            account.balance += tx_in.amount
        elif tx_in.type == "withdrawal":
            account.balance -= tx_in.amount
        # Record transaction
        tx = Transaction(account_id=account.id, amount=tx_in.amount, type=tx_in.type)
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return tx

    def list_transactions(self, db: Session, account_id: int, customer_id: int) -> List[Transaction]:
        account = db.query(DepositAccount).filter(DepositAccount.id == account_id).first()
        if not account or account.customer_id != customer_id:
            raise ValueError("Account not found or access denied")
        return db.query(Transaction).filter(Transaction.account_id == account_id).all()
