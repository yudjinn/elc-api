from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, select, func, Enum
from sqlalchemy.orm import column_property, relationship
import uuid

from .base import Base
from app.utils import StatusEnum

if TYPE_CHECKING:
    from .transaction import Transaction  # noqa: F401


class Bank(Base):
    name = Column(String(64), nullable=False)
    status = Column("status", Enum(StatusEnum))
    company_id = Column(uuid.UUID(as_uuid=True), ForeignKey("company.id"))

    company = relationship("Company", back_populates="bank")
    transactions = relationship("Transaction", back_populates="bank")

    balance = column_property(
        select(func.sum(Transaction.amount)).where(
            Transaction.bank_id == id and Transaction.status == StatusEnum.APPROVED
        )
    )
