from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any

_DATABASE_URL_PATTERN = re.compile(
    r"(?P<scheme>postgres(?:ql)?(?:\+\w+)?://)(?P<user>[^:\s/@]+):(?P<secret>[^@\s]+)@",
    flags=re.IGNORECASE,
)
_SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)(password|token|secret|api[_-]?key)(\s*[=:]\s*)([^\s,;]+)"
)


def redact_secrets(value: str) -> str:
    """Redact common credential forms before records are emitted."""
    value = _DATABASE_URL_PATTERN.sub(r"\g<scheme>\g<user>:***@", value)
    return _SECRET_ASSIGNMENT_PATTERN.sub(
        lambda match: f"{match.group(1)}{match.group(2)}***", value
    )


class JsonFormatter(logging.Formatter):
    """Small UTC JSON formatter for local services and future jobs."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": redact_secrets(record.getMessage()),
        }
        if record.exc_info:
            payload["exception"] = redact_secrets(self.formatException(record.exc_info))
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def configure_logging(level: str | int = "INFO") -> None:
    """Configure one application-owned structured root handler."""
    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, "name", None) == "ev_scanner_json":
            root.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.name = "ev_scanner_json"
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)
    root.setLevel(level)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
