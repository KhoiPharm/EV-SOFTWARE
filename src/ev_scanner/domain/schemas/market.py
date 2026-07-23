from __future__ import annotations

from typing import Self
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from ev_scanner.domain.enums import MarketStatus, MarketType, PriceSide
from ev_scanner.domain.schemas.base import AwareDatetime, DomainRecord, MoneyDecimal, OddsDecimal


class MarketSnapshotRecord(DomainRecord):
    race_id: UUID
    data_source_id: UUID
    market_type: MarketType
    source_market_id: str = Field(min_length=1, max_length=255)
    captured_at: AwareDatetime
    market_status: MarketStatus
    in_play: bool = False
    total_matched: MoneyDecimal | None = None
    latency_ms: int | None = Field(default=None, ge=0)
    runner_count: int = Field(ge=0)
    checksum: str | None = Field(default=None, max_length=128)


class PriceQuoteRecord(DomainRecord):
    race_id: UUID
    runner_id: UUID
    data_source_id: UUID
    market_snapshot_id: UUID | None = None
    market_type: MarketType
    side: PriceSide
    odds: OddsDecimal
    available_size: MoneyDecimal | None = None
    quoted_at: AwareDatetime
    received_at: AwareDatetime
    is_in_play: bool = False
    currency: str = Field(default="AUD", min_length=3, max_length=3)
    source_market_id: str | None = Field(default=None, max_length=255)
    market_status: MarketStatus

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def validate_quote_order(self) -> Self:
        if self.received_at < self.quoted_at:
            raise ValueError("received_at must not precede quoted_at")
        return self
