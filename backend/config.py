"""Configuration settings for the banking backend.

This module uses Pydantic's BaseSettings to load configuration from environment
variables or a .env file.  It contains settings for the database, JWT
authentication, and other application wide constants.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application configuration.

    The settings are loaded from environment variables.  For local
    development a ``.env`` file can be placed in the project root.
    """

    # Database
    DATABASE_URL: str = Field(
        "sqlite:///./banking.db", description="SQLAlchemy database URL"
    )

    # JWT
    JWT_SECRET_KEY: str = Field(
        "super-secret-key",
        description="Secret key used to sign JWT tokens",
    )
    JWT_ALGORITHM: str = Field("HS256", description="JWT signing algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        30, description="Access token expiration time in minutes"
    )

    # Application
    PROJECT_NAME: str = Field("Banking App", description="Project name")
    VERSION: str = Field("0.1.0", description="API version")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Singleton instance used throughout the application
settings = Settings()
