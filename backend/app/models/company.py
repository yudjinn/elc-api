from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from .base import Base


# If type checking, import models
if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .file import File  # noqa: F401


class Company(Base):
    name = Column(String(128), nullable=False)
    logo_id = Column(uuid.UUID(as_uuid=True), ForeignKey("file.id"))

    members = relationship("User", back_populates="company")
    logo = relationship("File", back_populates="company")
