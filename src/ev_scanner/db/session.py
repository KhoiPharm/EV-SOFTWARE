from __future__ import annotations

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from ev_scanner.db.engine import get_engine


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    """Yield a request-scoped session without creating one at import time."""
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
