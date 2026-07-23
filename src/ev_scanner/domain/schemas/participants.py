from __future__ import annotations

from datetime import date

from pydantic import Field, field_validator

from ev_scanner.domain.enums import HorseSex
from ev_scanner.domain.schemas.base import NamedRecord


class HorseRecord(NamedRecord):
    foaling_date: date | None = None
    sex: HorseSex = HorseSex.UNKNOWN
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    sire_name: str | None = Field(default=None, max_length=255)
    dam_name: str | None = Field(default=None, max_length=255)
    active: bool = True

    @field_validator("country_code")
    @classmethod
    def uppercase_optional_country(cls, value: str | None) -> str | None:
        return value.upper() if value is not None else None


class JockeyRecord(NamedRecord):
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    active: bool = True

    @field_validator("country_code")
    @classmethod
    def uppercase_optional_country(cls, value: str | None) -> str | None:
        return value.upper() if value is not None else None


class TrainerRecord(NamedRecord):
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    active: bool = True

    @field_validator("country_code")
    @classmethod
    def uppercase_optional_country(cls, value: str | None) -> str | None:
        return value.upper() if value is not None else None
