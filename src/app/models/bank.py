from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, select, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.hybrid import hybrid_property

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

    @hybrid_property
    def balance(self):
        return sum(t.amount for t in self.transactions)
