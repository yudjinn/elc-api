from typing import Optional

from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

# Shared Properties
class FileBase(SQLModel):
    file_name: str
    file_size: str


# Properties to recieve via API on creation
class FileCreate(FileBase):
    pass


# Properties to recieve via API on update
class FileUpdate(FileBase):
    pass


# Properties shared by models stored in db
class FileInDBBase(FileBase):
    id: uuid.UUID
    updated_dt: datetime
    created_dt: datetime

    class Config:
        orm_mode = True


# Additional Properties to return via API
class File(FileInDBBase):
    pass


# Additional properties stored in db
class FileInDB(FileInDBBase):
    pass
