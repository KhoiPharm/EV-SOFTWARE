from __future__ import annotations

from typing import cast

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ev_scanner.api.routes.health import get_database_checker
from ev_scanner.core.errors import DatabaseUnavailableError


def test_liveness_does_not_require_database(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "live"}


def test_readiness_success(client: TestClient) -> None:
    app = cast(FastAPI, client.app)
    app.dependency_overrides[get_database_checker] = lambda: lambda: None

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "checks": {"database": "available"}}


def test_readiness_failure_is_sanitized(client: TestClient) -> None:
    def unavailable() -> None:
        raise DatabaseUnavailableError("postgresql://user:password@private-host/database")

    app = cast(FastAPI, client.app)
    app.dependency_overrides[get_database_checker] = lambda: unavailable

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {"database": "unavailable"},
    }
    assert "password" not in response.text
    assert "private-host" not in response.text
