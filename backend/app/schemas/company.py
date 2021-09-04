from typing import Optional

from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

# Shared Properties
class CompanyBase(SQLModel):
    name: str


# Properties to recieve via API on creation
class CompanyCreate(CompanyBase):
    pass


# Properties to recieve via API on update
class CompanyUpdate(CompanyBase):
    pass


# Properties shared by models stored in db
class CompanyInDBBase(CompanyBase):
    id: uuid.UUID
    updated_dt: datetime
    created_dt: datetime

    logo_id: Optional[uuid.UUID] = Field(default=None)

    class Config:
        orm_mode = True


# Additional Properties to return via API
class Company(CompanyInDBBase):
    pass


# Additional properties stored in db
class CompanyInDB(CompanyInDBBase):
    pass
