from typing import Optional

from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

# Shared Properties
class BankBase(SQLModel):
    name: str
    status: str


# Properties to recieve via API on creation
class BankCreate(BankBase):
    pass


# Properties to recieve via API on update
class BankUpdate(BankBase):
    pass


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
    balance : float


# Additional properties stored in db
class BankInDB(BankInDBBase):
    pass
