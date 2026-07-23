from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import DataQualityStatus, EntityType, SourceType, SurfaceType
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class DataSource(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "data_sources"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    source_type: Mapped[SourceType] = mapped_column(
        Enum(
            SourceType,
            name="source_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    base_url: Mapped[str | None] = mapped_column(String(512))
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )


class ExternalIdentifier(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "external_identifiers"
    __table_args__ = (
        UniqueConstraint(
            "data_source_id", "entity_type", "external_id", name="external_identifier_scope"
        ),
        CheckConstraint("last_seen_at >= first_seen_at", name="last_seen_after_first_seen"),
        Index("ix_external_identifiers_internal", "entity_type", "internal_entity_id"),
    )

    data_source_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False
    )
    entity_type: Mapped[EntityType] = mapped_column(
        Enum(
            EntityType,
            name="entity_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    internal_entity_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str | None] = mapped_column(String(255))
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProvenanceRecord(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "provenance_records"
    __table_args__ = (
        Index("ix_provenance_entity", "entity_type", "internal_entity_id"),
        CheckConstraint("ingested_at >= source_timestamp", name="ingested_after_source"),
    )

    data_source_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False
    )
    entity_type: Mapped[EntityType] = mapped_column(
        Enum(
            EntityType,
            name="provenance_entity_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    internal_entity_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    source_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_reference: Mapped[str] = mapped_column(Text, nullable=False)
    adapter_version: Mapped[str] = mapped_column(String(64), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(64), nullable=False)
    transformation_lineage: Mapped[dict[str, object]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb")
    )
    quality_status: Mapped[DataQualityStatus] = mapped_column(
        Enum(
            DataQualityStatus,
            name="data_quality_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    quality_notes: Mapped[str | None] = mapped_column(Text)


class Track(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tracks"
    __table_args__ = (
        UniqueConstraint(
            "normalized_name", "state_code", "country_code", name="track_identity"
        ),
        CheckConstraint("latitude IS NULL OR latitude BETWEEN -90 AND 90", name="latitude_range"),
        CheckConstraint(
            "longitude IS NULL OR longitude BETWEEN -180 AND 180", name="longitude_range"
        ),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    state_code: Mapped[str] = mapped_column(String(8), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, default="AU")
    timezone: Mapped[str] = mapped_column(
        String(64), nullable=False, default="Australia/Sydney"
    )
    surface_type: Mapped[SurfaceType] = mapped_column(
        Enum(
            SurfaceType,
            name="surface_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=SurfaceType.TURF,
    )
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
