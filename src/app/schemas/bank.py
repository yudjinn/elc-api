from typing import Optional

from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

from app.utils import StatusEnum

# Shared Properties
class BankBase(SQLModel):
    name: str
    status: StatusEnum
    company_id: uuid.UUID


# Properties to recieve via API on creation
class BankCreate(BankBase):
    name: Optional[str] = Field(default=None)
    status: Optional[StatusEnum] = Field(default=StatusEnum.ACTIVE)


# Properties to recieve via API on update
class BankUpdate(BankBase):
    name: Optional[str] = Field(default=None)
    status: Optional[StatusEnum] = Field(default=StatusEnum.ACTIVE)


# Properties shared by models stored in db
class BankInDBBase(BankBase):
    id: uuid.UUID
    updated_dt: datetime
    created_dt: datetime

    company_id: uuid.UUID

    class Config:
        orm_mode = True


# Additional Properties to return via API
class Bank(BankInDBBase):
    balance: float


# Additional properties stored in db
class BankInDB(BankInDBBase):
    pass
