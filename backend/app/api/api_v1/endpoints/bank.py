from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import RankEnum

router = APIRouter()


@router.get("/", response_model=List[models.Bank])
def read_all_by_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all banks attached to company by user
    """
    if banks := crud.bank.get_all_by_company(db, user=current_user) is None:
        # No Company Error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not part of a company.",
        )
    return banks


@router.get("/{id}", response_model=schemas.Bank)
def read_bank(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get bank by id
    """
    bank = crud.bank.get(db=db, id=id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found."
        )
    if current_user.company_id != bank.company_id:
        raise HTTPException(
            status_code=404, detail="User does not have access to that bank."
        )
    if not crud.user.is_superuser(current_user) and (
        bank.company_id != current_user.company_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    return bank


@router.post("/", response_model=schemas.Bank)
def create_bank(
    *,
    db: Session = Depends(deps.get_db),
    bank_in: schemas.BankCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new bank
    """
    if not current_user.company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User has no company"
        )
    if current_user.rank < RankEnum.CONSUL:
        raise HTTPException(
            status_code=400, detail="User must be at least CONSUL to make banks."
        )
    bank = crud.bank.create(db=db, obj_in=bank_in, company_id=current_user.company_id)
    return bank


@router.put("/{id}", response_model=schemas.Bank)
def update_bank(
    *,
    db: Session = Depends(deps.get_bd),
    id: uuid.UUID,
    bank_in: schemas.BankUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update bank
    """
    bank = crud.bank.get(db=db, id=id)
    if bank_in.company_id and bank_in.company_id != bank.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot change company id."
        )
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    if current_user.rank < RankEnum.CONSUL:
        raise HTTPException(
            status_code=400, detail="User must be at least CONSUL to edit banks."
        )
    bank = crud.bank.update(db=db, db_obj=bank, obj_in=bank_in)
    return bank


@router.delete("/{id}", response_model=schemas.Bank)
def delete_bank(
    *,
    db: Session = Depends(deps.get_bd),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an item.
    """
    if current_user.rank < RankEnum.GOVERNOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must be GOVERNOR to delete banks",
        )
    bank = crud.bank.get(db=db, id=id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found."
        )
    if current_user.company_id != bank.company_id:
        raise HTTPException(
            status_code=404, detail="User does not have access to that bank."
        )
    bank = crud.bank.remove(db=db, id=id)
    return bank
