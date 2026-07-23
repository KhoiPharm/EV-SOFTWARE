from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated, cast
from uuid import UUID, uuid4

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
)

from ev_scanner.domain.normalization import normalize_racing_name


def _to_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime values must be timezone-aware")
    return value.astimezone(timezone.utc)


def _reject_binary_float(value: object) -> object:
    if isinstance(value, float):
        raise ValueError("binary floating-point input is not accepted; use Decimal or a string")
    return value


AwareDatetime = Annotated[datetime, AfterValidator(_to_utc)]
OddsDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(gt=Decimal("1"), max_digits=12, decimal_places=4),
]
MoneyDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(ge=Decimal("0"), max_digits=16, decimal_places=2),
]
WeightDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(gt=Decimal("0"), max_digits=5, decimal_places=2),
]
NonNegativeWeightDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(ge=Decimal("0"), max_digits=5, decimal_places=2),
]
RatingDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(max_digits=8, decimal_places=3),
]
MarginDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(max_digits=8, decimal_places=3),
]
PositiveSecondsDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(gt=Decimal("0"), max_digits=7, decimal_places=3),
]
CoordinateDecimal = Annotated[
    Decimal,
    BeforeValidator(_reject_binary_float),
    Field(max_digits=9, decimal_places=6),
]


class DomainRecord(BaseModel):
    model_config = ConfigDict(
        extra="forbid", from_attributes=True, validate_default=True, str_strip_whitespace=True
    )

    id: UUID = Field(default_factory=uuid4)


class NamedRecord(DomainRecord):
    name: str = Field(min_length=1, max_length=255)
    normalized_name: str | None = Field(default=None, min_length=1, max_length=255)

    @field_validator("normalized_name", mode="after")
    @classmethod
    def normalize_name(cls, value: str | None, info: ValidationInfo) -> str:
        source = value if value is not None else cast(str, info.data["name"])
        normalized = normalize_racing_name(source)
        if not normalized:
            raise ValueError("name must contain at least one letter or digit")
        return normalized
