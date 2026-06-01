"""Expose API routers for the FastAPI application.

This module imports the individual router modules so that they can be
included in the main application via ``from .api import auth_router``.
"""

from .auth_router import router as auth_router
from .account_router import router as account_router
from .transaction_router import router as transaction_router
