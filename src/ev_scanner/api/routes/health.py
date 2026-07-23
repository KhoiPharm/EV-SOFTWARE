from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ev_scanner.api.schemas.health import LiveResponse, ReadyResponse
from ev_scanner.core.errors import DatabaseUnavailableError
from ev_scanner.db.health import check_database

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])
DatabaseChecker = Callable[[], None]


def get_database_checker() -> DatabaseChecker:
    """Return the replaceable readiness dependency."""
    return check_database


@router.get("/live", response_model=LiveResponse)
def liveness() -> LiveResponse:
    """Report process-level liveness without touching infrastructure."""
    return LiveResponse(status="live")


@router.get(
    "/ready",
    response_model=ReadyResponse,
    responses={503: {"model": ReadyResponse}},
)
def readiness(
    database_checker: Annotated[DatabaseChecker, Depends(get_database_checker)],
) -> ReadyResponse | JSONResponse:
    """Report whether required local infrastructure is usable."""
    try:
        database_checker()
    except DatabaseUnavailableError:
        logger.warning("database_readiness_check_failed")
        payload = ReadyResponse(status="not_ready", checks={"database": "unavailable"})
        return JSONResponse(status_code=503, content=payload.model_dump())
    return ReadyResponse(status="ready", checks={"database": "available"})
