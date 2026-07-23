from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ev_scanner.core.errors import DatabaseUnavailableError
from ev_scanner.db.engine import get_engine


def check_database() -> None:
    """Execute the minimum readiness query and return no provider details."""
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise DatabaseUnavailableError("Database readiness check failed.") from exc
