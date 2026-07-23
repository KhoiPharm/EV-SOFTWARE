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
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import ResultStatus
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class RaceResult(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "race_results"
    __table_args__ = (
        UniqueConstraint("runner_id", name="runner_result"),
        CheckConstraint(
            "finishing_position IS NULL OR finishing_position > 0",
            name="positive_finish_position",
        ),
        CheckConstraint(
            "starting_price IS NULL OR starting_price > 1", name="valid_starting_price"
        ),
    )

    race_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("races.id"), nullable=False
    )
    runner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("runners.id"), nullable=False
    )
    finishing_position: Mapped[int | None] = mapped_column(SmallInteger)
    finishing_margin_lengths: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    starting_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    result_status: Mapped[ResultStatus] = mapped_column(
        Enum(
            ResultStatus,
            name="result_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=ResultStatus.PROVISIONAL,
    )
    official: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
