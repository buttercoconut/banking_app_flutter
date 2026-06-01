"""FastAPI application entry point.

The app imports routers for customers, accounts and transactions.
"""

from fastapi import FastAPI

from .api import customers, accounts, transactions

app = FastAPI(title="Banking App Backend")

app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Banking API"}
