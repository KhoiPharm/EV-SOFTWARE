from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Enum, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from ev_scanner.db.base import Base
from ev_scanner.domain.enums import HorseSex
from ev_scanner.domain.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Horse(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "horses"
    __table_args__ = (Index("ix_horses_normalized_name", "normalized_name"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    foaling_date: Mapped[date | None] = mapped_column(Date)
    sex: Mapped[HorseSex] = mapped_column(
        Enum(
            HorseSex,
            name="horse_sex",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=HorseSex.UNKNOWN,
    )
    country_code: Mapped[str | None] = mapped_column(String(2))
    sire_name: Mapped[str | None] = mapped_column(String(255))
    dam_name: Mapped[str | None] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )


class Jockey(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "jockeys"
    __table_args__ = (Index("ix_jockeys_normalized_name", "normalized_name"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(2))
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )


class Trainer(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "trainers"
    __table_args__ = (Index("ix_trainers_normalized_name", "normalized_name"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(2))
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
