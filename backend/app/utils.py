from enum import Enum, IntEnum


class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PENDING = "PENDING"
    DELETED = "DELETED"
    APPROVED = "APPROVED"


class RankEnum(IntEnum):
    SETTLER = 1
    OFFICER = 2
    CONSUL = 3
    GOVERNOR = 4
