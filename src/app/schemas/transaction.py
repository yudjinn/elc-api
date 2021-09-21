from typing import Optional

from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

from app.utils import StatusEnum

# Shared Properties
class TransactionBase(SQLModel):
    amount: float
    status: StatusEnum


# Properties to recieve via API on creation
class TransactionCreate(TransactionBase):
    status: Optional[StatusEnum] = Field(default=StatusEnum.PENDING)


# Properties to recieve via API on update
class TransactionUpdate(TransactionBase):
    amount: Optional[float] = Field(default=None)
    status: Optional[StatusEnum] = Field(default=StatusEnum.PENDING)


# Properties shared by models stored in db
class TransactionInDBBase(TransactionBase):
    id: uuid.UUID
    updated_dt: datetime
    created_dt: datetime

    bank_id: uuid.UUID
    creator_id: uuid.UUID
    approver_id: Optional[uuid.UUID] = Field(default=None)

    class Config:
        orm_mode = True


# Additional Properties to return via API
class Transaction(TransactionInDBBase):
    pass


# Additional properties stored in db
class TransactionInDB(TransactionInDBBase):
    pass
