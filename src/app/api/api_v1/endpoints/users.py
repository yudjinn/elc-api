from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette_discord import DiscordOAuthClient
import uuid

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import RankEnum

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    in_game_name: str = Body(None),
    username: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if in_game_name is not None:
        user_in.in_game_name = in_game_name
    if username is not None:
        user_in.username = username
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    if "rank" in user_in:
        del user_in.rank
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.put("/{user_id}/{rank}", response_model=schemas.User)
def update_rank(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    rank: RankEnum,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    if rank.value == RankEnum.GOVERNOR.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot promote to governor, try transfer of ownership.")
    user = crud.user.get(db=db, id=user_id)
    if not user or not user.company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company or user not found."
        )
    if not current_user.rank or current_user.rank.value < RankEnum.CONSUL.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must be CONSUL or higher to promote members",
        )
    if current_user.company_id != user.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to this company.",
        )
    user = crud.user.update_rank(db=db, db_obj=user, rank=rank)
    return user


# Link Discord Account
discord_client = DiscordOAuthClient(
    settings.DISCORD_CLIENT_ID, settings.DISCORD_SECRET_KEY, settings.DISCORD_REDIRECT
)

# Discord login
@router.get("/link-discord", response_model=schemas.User)
async def link_discord(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return discord_client.redirect()


@router.get("/link-discord-callback", response_model=schemas.User)
async def finish_link(
    code: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    discord_user = await discord_client.login(code)
    user = crud.user.update(
        db,
        db_obj=current_user,
        obj_in={"discord_id": discord_user.id, "discord_name": discord_user.username},
    )
    return user
