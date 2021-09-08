from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .company import Company


class File(Base):
    file_name = Column(String(256), nullable=False)
    file_size = Column(Integer, nullable=False)

    company = relationship("Company", back_populates="logo")
