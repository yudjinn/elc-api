from enum import Enum


class StatusEnum(Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PENDING = "PENDING"
    DELETED = "DELETED"
    APPROVED = "APPROVED"


class RankEnum(Enum):
    SETTLER = "SETTLER"
    OFFICER = "OFFICER"
    CONSUL = "CONSUL"
    GOVERNOR = "GOVERNOR"
