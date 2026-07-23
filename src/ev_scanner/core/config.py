from __future__ import annotations

import logging
from functools import lru_cache
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ev_scanner.core.errors import ConfigurationError

_VALID_LOG_LEVELS = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}


class Settings(BaseSettings):
    """Canonical environment-backed application configuration."""

    model_config = SettingsConfigDict(
        env_prefix="EV_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    environment: Literal["development", "test", "production"] = "development"
    application_name: str = "EV Scanner"
    log_level: str = "INFO"
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    database_url: SecretStr = SecretStr(
        "postgresql+psycopg://ev_scanner:local_dev_only@127.0.0.1:5432/ev_scanner"
    )
    presentation_timezone: str = "Australia/Sydney"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in _VALID_LOG_LEVELS:
            raise ValueError(f"log_level must be one of {sorted(_VALID_LOG_LEVELS)}")
        return normalized

    @field_validator("presentation_timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("presentation_timezone must be a valid IANA timezone") from exc
        return value

    @property
    def logging_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings()
    except Exception as exc:
        raise ConfigurationError("Application configuration is invalid.") from exc
