from __future__ import annotations

from fastapi import FastAPI
from pytest import MonkeyPatch

from ev_scanner.api.app import create_app
from ev_scanner.core.config import Settings


def test_create_app_does_not_create_database_engine(monkeypatch: MonkeyPatch) -> None:
    from ev_scanner.db import engine as engine_module

    def fail_if_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("database engine was created during application construction")

    monkeypatch.setattr(engine_module, "create_engine", fail_if_called)
    application = create_app(Settings(_env_file=None, environment="test"))

    assert isinstance(application, FastAPI)
