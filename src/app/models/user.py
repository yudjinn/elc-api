from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base
from app.utils import RankEnum


# If type checking, import models
if TYPE_CHECKING:
    from .company import Company  # noqa: F401
    from .transaction import Transaction  # noqa: F401


class User(Base):
    username = Column(String(64), nullable=False)
    in_game_name = Column(String(64), nullable=False)
    discord_name = Column(String(64))
    discord_id = Column(String(128))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"))
    rank = Column("status", Enum(RankEnum))
    hashed_password = Column(String(256))

    company = relationship("Company", back_populates="members")
    transactions = relationship(
        "Transaction",
        back_populates="creator",
        primaryjoin="Transaction.creator_id == User.id",
    )
    approved_transactions = relationship(
        "Transaction",
        back_populates="approver",
        primaryjoin="Transaction.approver_id == User.id",
    )
