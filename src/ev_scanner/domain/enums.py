from __future__ import annotations

from enum import StrEnum


class SourceType(StrEnum):
    BOOKMAKER = "bookmaker"
    EXCHANGE = "exchange"
    RACING_AUTHORITY = "racing_authority"
    FORM_PROVIDER = "form_provider"
    MANUAL = "manual"
    DERIVED = "derived"


class EntityType(StrEnum):
    TRACK = "track"
    MEETING = "meeting"
    RACE = "race"
    HORSE = "horse"
    JOCKEY = "jockey"
    TRAINER = "trainer"
    RUNNER = "runner"
    RACE_RESULT = "race_result"
    FORM_RECORD = "form_record"
    MARKET_SNAPSHOT = "market_snapshot"
    PRICE_QUOTE = "price_quote"


class DataQualityStatus(StrEnum):
    RAW = "raw"
    VALIDATED = "validated"
    PARTIAL = "partial"
    REJECTED = "rejected"
    CORRECTED = "corrected"


class MeetingStatus(StrEnum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    ABANDONED = "abandoned"


class RaceStatus(StrEnum):
    SCHEDULED = "scheduled"
    OPEN = "open"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    ABANDONED = "abandoned"


class RunnerStatus(StrEnum):
    ACTIVE = "active"
    SCRATCHED = "scratched"
    LATE_SCRATCHED = "late_scratched"
    EMERGENCY = "emergency"
    NON_RUNNER = "non_runner"
    FINISHED = "finished"


class TrackCondition(StrEnum):
    FIRM = "firm"
    GOOD = "good"
    SOFT = "soft"
    HEAVY = "heavy"
    SYNTHETIC = "synthetic"
    UNKNOWN = "unknown"


class SurfaceType(StrEnum):
    TURF = "turf"
    SYNTHETIC = "synthetic"
    DIRT = "dirt"
    UNKNOWN = "unknown"


class HorseSex(StrEnum):
    COLT = "colt"
    FILLY = "filly"
    GELDING = "gelding"
    MARE = "mare"
    STALLION = "stallion"
    RIG = "rig"
    UNKNOWN = "unknown"


class MarketType(StrEnum):
    WIN = "win"
    PLACE = "place"


class PriceSide(StrEnum):
    BACK = "back"
    LAY = "lay"


class MarketStatus(StrEnum):
    INACTIVE = "inactive"
    OPEN = "open"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    SETTLED = "settled"


class ResultStatus(StrEnum):
    PROVISIONAL = "provisional"
    OFFICIAL = "official"
    AMENDED = "amended"
    VOID = "void"
