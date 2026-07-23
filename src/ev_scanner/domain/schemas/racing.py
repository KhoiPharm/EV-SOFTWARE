from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Self
from uuid import UUID

from pydantic import Field, model_validator

from ev_scanner.domain.enums import (
    MeetingStatus,
    RaceStatus,
    ResultStatus,
    RunnerStatus,
    SurfaceType,
    TrackCondition,
)
from ev_scanner.domain.schemas.base import (
    AwareDatetime,
    DomainRecord,
    MarginDecimal,
    MoneyDecimal,
    NonNegativeWeightDecimal,
    OddsDecimal,
    PositiveSecondsDecimal,
    RatingDecimal,
    WeightDecimal,
)


class MeetingRecord(DomainRecord):
    track_id: UUID
    meeting_date: date
    name: str | None = Field(default=None, max_length=255)
    status: MeetingStatus = MeetingStatus.SCHEDULED
    rail_position: str | None = Field(default=None, max_length=255)
    track_condition: TrackCondition | None = None
    weather: str | None = Field(default=None, max_length=255)
    scheduled_first_race_at: AwareDatetime | None = None


class RaceRecord(DomainRecord):
    meeting_id: UUID
    race_number: int = Field(ge=1, le=30)
    name: str | None = Field(default=None, max_length=255)
    scheduled_start_at: AwareDatetime
    actual_start_at: AwareDatetime | None = None
    distance_metres: int = Field(gt=0)
    race_class: str | None = Field(default=None, max_length=128)
    status: RaceStatus = RaceStatus.SCHEDULED
    track_condition: TrackCondition | None = None
    surface_type: SurfaceType | None = None
    field_size: int | None = Field(default=None, ge=0)
    rail_position: str | None = Field(default=None, max_length=255)
    prize_money: MoneyDecimal | None = None


class RunnerRecord(DomainRecord):
    race_id: UUID
    horse_id: UUID
    jockey_id: UUID | None = None
    trainer_id: UUID | None = None
    saddlecloth_number: int = Field(ge=1, le=99)
    barrier: int | None = Field(default=None, ge=1, le=99)
    weight_kg: WeightDecimal
    apprentice_claim_kg: NonNegativeWeightDecimal = Decimal("0")
    status: RunnerStatus = RunnerStatus.ACTIVE
    gear_changes: str | None = None
    emergency: bool = False

    @model_validator(mode="after")
    def validate_claim(self) -> Self:
        if self.apprentice_claim_kg > self.weight_kg:
            raise ValueError("apprentice_claim_kg must not exceed weight_kg")
        return self


class RaceResultRecord(DomainRecord):
    race_id: UUID
    runner_id: UUID
    finishing_position: int | None = Field(default=None, gt=0)
    finishing_margin_lengths: MarginDecimal | None = None
    starting_price: OddsDecimal | None = None
    result_status: ResultStatus = ResultStatus.PROVISIONAL
    official: bool = False


class FormRecordSchema(DomainRecord):
    horse_id: UUID
    race_id: UUID
    runner_id: UUID
    jockey_id: UUID | None = None
    trainer_id: UUID | None = None
    start_time: AwareDatetime
    finishing_position: int | None = Field(default=None, gt=0)
    finishing_margin_lengths: MarginDecimal | None = None
    distance_metres: int = Field(gt=0)
    track_condition: TrackCondition | None = None
    barrier: int | None = Field(default=None, ge=1, le=99)
    weight_kg: WeightDecimal | None = None
    starting_price: OddsDecimal | None = None
    speed_rating: RatingDecimal | None = None
    early_speed_rating: RatingDecimal | None = None
    late_speed_rating: RatingDecimal | None = None
    final_600m_seconds: PositiveSecondsDecimal | None = None
    source_data_complete: bool = False
