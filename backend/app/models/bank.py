from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, select, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from .base import Base
from app.utils import StatusEnum
from .transaction import Transaction

if TYPE_CHECKING:
    pass


class Bank(Base):
    name = Column(String(64), nullable=False)
    status = Column("status", Enum(StatusEnum))
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"))

    company = relationship("Company", back_populates="banks")
    transactions = relationship(
        "Transaction", back_populates="bank", cascade="all, delete"
    )

    balance = column_property(
        select(func.sum(Transaction.amount))
        .where(Transaction.bank_id == id and Transaction.status == StatusEnum.APPROVED)
        .scalar_subquery()
    )
