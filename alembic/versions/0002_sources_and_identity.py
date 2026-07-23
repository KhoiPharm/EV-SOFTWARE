"""Create canonical source, identity, provenance, and track tables.

Revision ID: 0002_sources_and_identity
Revises: 0001_bootstrap
Create Date: 2026-07-24
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_sources_and_identity"
down_revision: str | None = "0001_bootstrap"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

source_type = sa.Enum(
    "BOOKMAKER",
    "EXCHANGE",
    "RACING_AUTHORITY",
    "FORM_PROVIDER",
    "MANUAL",
    "DERIVED",
    name="source_type",
    native_enum=False,
    create_constraint=True,
)
entity_type = sa.Enum(
    "TRACK",
    "MEETING",
    "RACE",
    "HORSE",
    "JOCKEY",
    "TRAINER",
    "RUNNER",
    "RACE_RESULT",
    "FORM_RECORD",
    "MARKET_SNAPSHOT",
    "PRICE_QUOTE",
    name="entity_type",
    native_enum=False,
    create_constraint=True,
)
provenance_entity_type = sa.Enum(
    "TRACK",
    "MEETING",
    "RACE",
    "HORSE",
    "JOCKEY",
    "TRAINER",
    "RUNNER",
    "RACE_RESULT",
    "FORM_RECORD",
    "MARKET_SNAPSHOT",
    "PRICE_QUOTE",
    name="provenance_entity_type",
    native_enum=False,
    create_constraint=True,
)
data_quality_status = sa.Enum(
    "RAW",
    "VALIDATED",
    "PARTIAL",
    "REJECTED",
    "CORRECTED",
    name="data_quality_status",
    native_enum=False,
    create_constraint=True,
)
surface_type = sa.Enum(
    "TURF",
    "SYNTHETIC",
    "DIRT",
    "UNKNOWN",
    name="surface_type",
    native_enum=False,
    create_constraint=True,
)


def _identity_columns() -> list[sa.Column[object]]:
    return [
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    ]


def upgrade() -> None:
    op.create_table(
        "data_sources",
        *_identity_columns(),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("source_type", source_type, nullable=False),
        sa.Column("base_url", sa.String(length=512), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_data_sources")),
        sa.UniqueConstraint("slug", name=op.f("uq_data_sources_slug")),
    )
    op.create_table(
        "tracks",
        *_identity_columns(),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=False),
        sa.Column("state_code", sa.String(length=8), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("surface_type", surface_type, nullable=False),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.CheckConstraint(
            "latitude IS NULL OR latitude BETWEEN -90 AND 90",
            name=op.f("ck_tracks_latitude_range"),
        ),
        sa.CheckConstraint(
            "longitude IS NULL OR longitude BETWEEN -180 AND 180",
            name=op.f("ck_tracks_longitude_range"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tracks")),
        sa.UniqueConstraint(
            "normalized_name", "state_code", "country_code", name="track_identity"
        ),
    )
    op.create_table(
        "external_identifiers",
        *_identity_columns(),
        sa.Column("data_source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_type", entity_type, nullable=False),
        sa.Column("internal_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "last_seen_at >= first_seen_at",
            name=op.f("ck_external_identifiers_last_seen_after_first_seen"),
        ),
        sa.ForeignKeyConstraint(
            ["data_source_id"],
            ["data_sources.id"],
            name=op.f("fk_external_identifiers_data_source_id_data_sources"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_external_identifiers")),
        sa.UniqueConstraint(
            "data_source_id", "entity_type", "external_id", name="external_identifier_scope"
        ),
    )
    op.create_index(
        "ix_external_identifiers_internal",
        "external_identifiers",
        ["entity_type", "internal_entity_id"],
        unique=False,
    )
    op.create_table(
        "provenance_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("data_source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_type", provenance_entity_type, nullable=False),
        sa.Column("internal_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_reference", sa.Text(), nullable=False),
        sa.Column("adapter_version", sa.String(length=64), nullable=False),
        sa.Column("schema_version", sa.String(length=64), nullable=False),
        sa.Column(
            "transformation_lineage",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("quality_status", data_quality_status, nullable=False),
        sa.Column("quality_notes", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "ingested_at >= source_timestamp",
            name=op.f("ck_provenance_records_ingested_after_source"),
        ),
        sa.ForeignKeyConstraint(
            ["data_source_id"],
            ["data_sources.id"],
            name=op.f("fk_provenance_records_data_source_id_data_sources"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_provenance_records")),
    )
    op.create_index(
        "ix_provenance_entity",
        "provenance_records",
        ["entity_type", "internal_entity_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_provenance_entity", table_name="provenance_records")
    op.drop_table("provenance_records")
    op.drop_index("ix_external_identifiers_internal", table_name="external_identifiers")
    op.drop_table("external_identifiers")
    op.drop_table("tracks")
    op.drop_table("data_sources")
