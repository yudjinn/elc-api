from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.db.session import engine
from app.db import base  # noqa: F401
from app.models.base import Base
from app.utils import RankEnum


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)  # needs engine first

    # Init first user if in dev mode
    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        # create user object
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            in_game_name="BNK_ADMIN",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        # save change to db
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
