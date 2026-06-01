"""Database models for the banking backend.

The models are defined using SQLAlchemy's declarative base.  They are
kept in a separate module so that the API layer can import them
without pulling in the entire database setup.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..config import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("DepositAccount", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.name} ({self.email})>"


class DepositAccount(Base):
    __tablename__ = "deposit_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, nullable=False, index=True)
    balance = Column(Float, default=0.0, nullable=False)
    interest_rate = Column(Float, default=0.01, nullable=False)  # 1% per annum
    last_interest_applied = Column(DateTime, default=datetime.utcnow)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="accounts")

    transactions = relationship("Transaction", back_populates="account")

    def __repr__(self):
        return f"<DepositAccount {self.account_number} Balance:{self.balance:.2f}>"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("deposit_accounts.id"))
    account = relationship("DepositAccount", back_populates="transactions")

    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # "deposit", "withdrawal", "interest"
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.type} {self.amount} on {self.timestamp}>"
