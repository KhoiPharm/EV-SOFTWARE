from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import RaceStatus, SurfaceType, TrackCondition
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Race(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "races"
    __table_args__ = (
        UniqueConstraint("meeting_id", "race_number", name="meeting_race_number"),
        CheckConstraint("race_number BETWEEN 1 AND 30", name="race_number_range"),
        CheckConstraint("distance_metres > 0", name="positive_distance"),
        CheckConstraint("field_size IS NULL OR field_size >= 0", name="non_negative_field_size"),
        CheckConstraint("prize_money IS NULL OR prize_money >= 0", name="non_negative_prize"),
    )

    meeting_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("meetings.id"), nullable=False
    )
    race_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255))
    scheduled_start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    distance_metres: Mapped[int] = mapped_column(Integer, nullable=False)
    race_class: Mapped[str | None] = mapped_column(String(128))
    status: Mapped[RaceStatus] = mapped_column(
        Enum(
            RaceStatus,
            name="race_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=RaceStatus.SCHEDULED,
    )
    track_condition: Mapped[TrackCondition | None] = mapped_column(
        Enum(
            TrackCondition,
            name="race_track_condition",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
    surface_type: Mapped[SurfaceType | None] = mapped_column(
        Enum(
            SurfaceType,
            name="race_surface_type",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
    field_size: Mapped[int | None] = mapped_column(SmallInteger)
    rail_position: Mapped[str | None] = mapped_column(String(255))
    prize_money: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
