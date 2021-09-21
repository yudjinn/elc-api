from typing import Optional

from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

from app.utils import RankEnum

# Shared Properties
class UserBase(SQLModel):
    username: Optional[str] = Field(default=None)
    in_game_name: Optional[str] = Field(default=None)
    discord_name: Optional[str] = Field(default=None)
    discord_id: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    is_superuser: Optional[bool] = Field(default=False)
    company_id: Optional[uuid.UUID] = Field(default=None)
    rank: Optional[RankEnum] = Field(default=None)


# Properties to recieve via API on creation
class UserCreate(UserBase):
    password: Optional[str] = Field(default=None)


# Properties to recieve via API on update
class UserUpdate(UserBase):
    password: Optional[str] = Field(default=None)


class UserInDBBase(UserBase):
    id: uuid.UUID
    updated_dt: datetime
    created_dt: datetime

    class Config:
        orm_mode = True


# Additional Properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in db
class UserInDB(UserInDBBase):
    hashed_password: str
