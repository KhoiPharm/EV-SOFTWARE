from __future__ import annotations

from decimal import Decimal
from typing import Self
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import Field, field_validator, model_validator

from ev_scanner.domain.enums import DataQualityStatus, EntityType, SourceType, SurfaceType
from ev_scanner.domain.schemas.base import (
    AwareDatetime,
    CoordinateDecimal,
    DomainRecord,
    NamedRecord,
)


class DataSourceRecord(DomainRecord):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$", max_length=64)
    source_type: SourceType
    base_url: str | None = Field(default=None, max_length=512)
    active: bool = True


class ExternalIdentifierRecord(DomainRecord):
    data_source_id: UUID
    entity_type: EntityType
    internal_entity_id: UUID
    external_id: str = Field(min_length=1, max_length=255)
    normalized_name: str | None = Field(default=None, max_length=255)
    first_seen_at: AwareDatetime
    last_seen_at: AwareDatetime

    @model_validator(mode="after")
    def validate_seen_order(self) -> Self:
        if self.last_seen_at < self.first_seen_at:
            raise ValueError("last_seen_at must not precede first_seen_at")
        return self


class ProvenanceRecordSchema(DomainRecord):
    data_source_id: UUID
    entity_type: EntityType
    internal_entity_id: UUID
    source_timestamp: AwareDatetime
    ingested_at: AwareDatetime
    source_reference: str = Field(min_length=1)
    adapter_version: str = Field(min_length=1, max_length=64)
    schema_version: str = Field(min_length=1, max_length=64)
    transformation_lineage: dict[str, object] = Field(default_factory=dict)
    quality_status: DataQualityStatus
    quality_notes: str | None = None

    @model_validator(mode="after")
    def validate_ingestion_order(self) -> Self:
        if self.ingested_at < self.source_timestamp:
            raise ValueError("ingested_at must not precede source_timestamp")
        return self


class TrackRecord(NamedRecord):
    state_code: str = Field(min_length=2, max_length=8)
    country_code: str = Field(default="AU", min_length=2, max_length=2)
    timezone: str = Field(default="Australia/Sydney", min_length=1, max_length=64)
    surface_type: SurfaceType = SurfaceType.TURF
    latitude: CoordinateDecimal | None = None
    longitude: CoordinateDecimal | None = None
    active: bool = True

    @field_validator("state_code", "country_code")
    @classmethod
    def uppercase_codes(cls, value: str) -> str:
        return value.upper()

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("timezone must be a valid IANA timezone") from exc
        return value

    @model_validator(mode="after")
    def validate_coordinates(self) -> Self:
        if self.latitude is not None and not Decimal("-90") <= self.latitude <= Decimal("90"):
            raise ValueError("latitude must be between -90 and 90")
        if self.longitude is not None and not Decimal("-180") <= self.longitude <= Decimal("180"):
            raise ValueError("longitude must be between -180 and 180")
        return self
