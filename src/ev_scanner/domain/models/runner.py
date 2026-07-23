from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Enum,
    ForeignKey,
    Numeric,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import RunnerStatus
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Runner(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "runners"
    __table_args__ = (
        UniqueConstraint("race_id", "horse_id", name="race_horse"),
        UniqueConstraint("race_id", "saddlecloth_number", name="race_saddlecloth"),
        CheckConstraint("saddlecloth_number BETWEEN 1 AND 99", name="saddlecloth_range"),
        CheckConstraint("barrier IS NULL OR barrier BETWEEN 1 AND 99", name="barrier_range"),
        CheckConstraint("weight_kg > 0", name="positive_weight"),
        CheckConstraint("apprentice_claim_kg >= 0", name="non_negative_claim"),
        CheckConstraint("apprentice_claim_kg <= weight_kg", name="claim_not_above_weight"),
    )

    race_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("races.id"), nullable=False
    )
    horse_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("horses.id"), nullable=False
    )
    jockey_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("jockeys.id")
    )
    trainer_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("trainers.id")
    )
    saddlecloth_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    barrier: Mapped[int | None] = mapped_column(SmallInteger)
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    apprentice_claim_kg: Mapped[Decimal] = mapped_column(
        Numeric(4, 2), nullable=False, default=Decimal("0"), server_default=text("0")
    )
    status: Mapped[RunnerStatus] = mapped_column(
        Enum(
            RunnerStatus,
            name="runner_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=RunnerStatus.ACTIVE,
    )
    gear_changes: Mapped[str | None] = mapped_column(Text)
    emergency: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
