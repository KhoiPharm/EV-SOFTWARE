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
    Integer,
    Numeric,
    SmallInteger,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import TrackCondition
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class FormRecord(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "form_records"
    __table_args__ = (
        UniqueConstraint("runner_id", name="runner_form_record"),
        CheckConstraint("distance_metres > 0", name="form_positive_distance"),
        CheckConstraint(
            "barrier IS NULL OR barrier BETWEEN 1 AND 99", name="form_barrier_range"
        ),
        CheckConstraint("weight_kg IS NULL OR weight_kg > 0", name="form_positive_weight"),
        CheckConstraint(
            "starting_price IS NULL OR starting_price > 1", name="form_valid_price"
        ),
        CheckConstraint(
            "final_600m_seconds IS NULL OR final_600m_seconds > 0",
            name="positive_final_600m",
        ),
    )

    horse_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("horses.id"), nullable=False
    )
    race_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("races.id"), nullable=False
    )
    runner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("runners.id"), nullable=False
    )
    jockey_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("jockeys.id")
    )
    trainer_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("trainers.id")
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finishing_position: Mapped[int | None] = mapped_column(SmallInteger)
    finishing_margin_lengths: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    distance_metres: Mapped[int] = mapped_column(Integer, nullable=False)
    track_condition: Mapped[TrackCondition | None] = mapped_column(
        Enum(
            TrackCondition,
            name="form_track_condition",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
    barrier: Mapped[int | None] = mapped_column(SmallInteger)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    starting_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    speed_rating: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    early_speed_rating: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    late_speed_rating: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    final_600m_seconds: Mapped[Decimal | None] = mapped_column(Numeric(7, 3))
    source_data_complete: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
