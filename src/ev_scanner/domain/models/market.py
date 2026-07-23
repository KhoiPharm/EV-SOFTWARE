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
    Integer,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import MarketStatus, MarketType, PriceSide
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class MarketSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "market_snapshots"
    __table_args__ = (
        UniqueConstraint(
            "data_source_id", "source_market_id", "captured_at", name="source_market_capture"
        ),
        Index("ix_market_snapshots_race_captured", "race_id", "captured_at"),
        CheckConstraint(
            "total_matched IS NULL OR total_matched >= 0", name="non_negative_matched"
        ),
        CheckConstraint("latency_ms IS NULL OR latency_ms >= 0", name="non_negative_latency"),
        CheckConstraint("runner_count >= 0", name="non_negative_runner_count"),
    )

    race_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("races.id"), nullable=False
    )
    data_source_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False
    )
    market_type: Mapped[MarketType] = mapped_column(
        Enum(
            MarketType,
            name="market_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    source_market_id: Mapped[str] = mapped_column(String(255), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    market_status: Mapped[MarketStatus] = mapped_column(
        Enum(
            MarketStatus,
            name="market_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    in_play: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    total_matched: Mapped[Decimal | None] = mapped_column(Numeric(16, 2))
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    runner_count: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    checksum: Mapped[str | None] = mapped_column(String(128))


class PriceQuote(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "price_quotes"
    __table_args__ = (
        Index("ix_price_quotes_runner_quoted", "runner_id", "quoted_at"),
        CheckConstraint("odds > 1", name="valid_odds"),
        CheckConstraint(
            "available_size IS NULL OR available_size >= 0", name="non_negative_size"
        ),
        CheckConstraint("received_at >= quoted_at", name="received_after_quote"),
    )

    race_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("races.id"), nullable=False
    )
    runner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("runners.id"), nullable=False
    )
    data_source_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False
    )
    market_snapshot_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("market_snapshots.id")
    )
    market_type: Mapped[MarketType] = mapped_column(
        Enum(
            MarketType,
            name="quote_market_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    side: Mapped[PriceSide] = mapped_column(
        Enum(
            PriceSide,
            name="price_side",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    odds: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    available_size: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    quoted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_in_play: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="AUD")
    source_market_id: Mapped[str | None] = mapped_column(String(255))
    market_status: Mapped[MarketStatus] = mapped_column(
        Enum(
            MarketStatus,
            name="quote_market_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
    )
