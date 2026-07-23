from __future__ import annotations

import pytest
from pydantic import ValidationError

from ev_scanner.core.config import Settings


def test_settings_have_safe_local_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.host == "127.0.0.1"
    assert settings.presentation_timezone == "Australia/Sydney"
    assert "***" in repr(settings.database_url)


def test_log_level_is_normalized() -> None:
    settings = Settings(_env_file=None, log_level="warning")
    assert settings.log_level == "WARNING"


def test_invalid_timezone_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, presentation_timezone="Not/AZone")
