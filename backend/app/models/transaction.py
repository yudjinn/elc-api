from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import uuid

from .base import Base
from app.utils import StatusEnum

if TYPE_CHECKING:
    from .bank import Bank  # noqa: F401
    from .user import User  # noqa: F401


class Transaction(Base):
    amount = Column(Float, nullable=False)
    status = Column("status", Enum(StatusEnum))

    bank_id = Column(uuid.UUID(as_uuid=True), ForeignKey("bank.id"))
    creator_id = Column(uuid.UUID(as_uuid=True), ForeignKey("user.id"))
    approver_id = Column(uuid.UUID(as_uuid=True), ForeignKey("user.id"))

    bank = relationship("Bank", back_populates="transactions")
    creator = relationship(
        "User", back_populates="transactions", foreign_keys=[creator_id]
    )
    approver = relationship(
        "User", back_populates="approved_transactions", foreign_keys=[approver_id]
    )
