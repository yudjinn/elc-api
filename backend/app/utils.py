from enum import Enum


class StatusEnum(Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PENDING = "PENDING"
    DELETED = "DELETED"
    APPROVED = "APPROVED"


class RankEnum(Enum):
    SETTLER = 1
    OFFICER = 2
    CONSUL = 3
    GOVERNOR = 4
