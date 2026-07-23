from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ev_scanner.api.app import create_app
from ev_scanner.core.config import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(_env_file=None, environment="test", log_level="WARNING")


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(settings)) as test_client:
        yield test_client
