from typing import Any, Optional

from sqlalchemy import Column, DateTime
from sqlalchemy.orm.decl_api import as_declarative, declared_attr
import uuid
from datetime import datetime


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Optional[uuid.UUID] = Column(
        uuid.UUID(as_uuid=True), default=uuid.uuid1, primary_key=True
    )

    updated_dt: Optional[datetime] = Column(DateTime, default=datetime.utcnow)
    created_dt: Optional[datetime] = Column(DateTime, default=datetime.utcnow)
