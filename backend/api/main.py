"""FastAPI application entry point.

The app includes routers for authentication, account management and
transaction handling.  It also sets up the database connection and
provides a simple health‑check endpoint.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth_router, account_router, transaction_router
from ..config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Allow CORS for the Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(account_router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction_router, prefix="/transactions", tags=["transactions"])

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
