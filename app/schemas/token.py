from typing import Optional

from sqlmodel import SQLModel
import uuid


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: Optional[uuid.UUID] = None
