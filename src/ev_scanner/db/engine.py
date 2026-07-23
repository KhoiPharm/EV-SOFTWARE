from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Engine, create_engine

from ev_scanner.core.config import get_settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create the SQLAlchemy engine lazily on first database use."""
    settings = get_settings()
    return create_engine(
        settings.database_url.get_secret_value(),
        pool_pre_ping=True,
        future=True,
    )
