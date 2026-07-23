from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LiveResponse(ApiModel):
    status: Literal["live"]


class ReadyResponse(ApiModel):
    status: Literal["ready", "not_ready"]
    checks: dict[str, Literal["available", "unavailable"]]


class ErrorDetail(ApiModel):
    code: str
    message: str


class ErrorResponse(ApiModel):
    error: ErrorDetail
