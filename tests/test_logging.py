from __future__ import annotations

import json
import logging

from ev_scanner.core.logging import JsonFormatter, redact_secrets


def test_json_formatter_uses_required_fields() -> None:
    record = logging.LogRecord(
        name="ev_scanner.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="service started",
        args=(),
        exc_info=None,
    )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "ev_scanner.test"
    assert payload["message"] == "service started"
    assert payload["timestamp"].endswith("+00:00")


def test_redaction_removes_database_password_and_token() -> None:
    value = "postgresql+psycopg://user:topsecret@db/app token=abc123"

    redacted = redact_secrets(value)

    assert "topsecret" not in redacted
    assert "abc123" not in redacted
    assert "user:***@db" in redacted
