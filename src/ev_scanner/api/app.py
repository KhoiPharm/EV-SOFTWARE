from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ev_scanner.api.routes.health import router as health_router
from ev_scanner.api.schemas.health import ErrorDetail, ErrorResponse
from ev_scanner.core.config import Settings, get_settings
from ev_scanner.core.errors import AppError
from ev_scanner.core.logging import configure_logging

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construct the API without opening external connections."""
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings.log_level)

    application = FastAPI(
        title=resolved_settings.application_name,
        version="0.1.0",
        description="Local Australian thoroughbred racing EV decision-support service.",
    )
    application.state.settings = resolved_settings
    application.include_router(health_router)

    @application.exception_handler(AppError)
    async def handle_application_error(_: Request, exc: AppError) -> JSONResponse:
        logger.warning("application_error code=%s", exc.code)
        payload = ErrorResponse(error=ErrorDetail(code=exc.code, message=exc.public_message))
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @application.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unexpected_application_error", exc_info=exc)
        payload = ErrorResponse(
            error=ErrorDetail(code="internal_error", message="An unexpected error occurred.")
        )
        return JSONResponse(status_code=500, content=payload.model_dump())

    return application


app = create_app()
