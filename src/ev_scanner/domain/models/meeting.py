from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import MeetingStatus, TrackCondition
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Meeting(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "meetings"
    __table_args__ = (UniqueConstraint("track_id", "meeting_date", name="meeting_track_date"),)

    track_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tracks.id"), nullable=False
    )
    meeting_date: Mapped[date] = mapped_column(Date, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[MeetingStatus] = mapped_column(
        Enum(
            MeetingStatus,
            name="meeting_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=MeetingStatus.SCHEDULED,
    )
    rail_position: Mapped[str | None] = mapped_column(String(255))
    track_condition: Mapped[TrackCondition | None] = mapped_column(
        Enum(
            TrackCondition,
            name="meeting_track_condition",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
    weather: Mapped[str | None] = mapped_column(String(255))
    scheduled_first_race_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
