from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app import crud, models, schemas
from app.api import deps
from app.utils import RankEnum

router = APIRouter()


@router.get("/", response_model=schemas.Company)
def read_company(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company of user
    """
    company = crud.company.get(db=db, id=current_user.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have an associated company",
        )
    return company


@router.post("/", response_model=schemas.Company)
def create_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.CompanyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new company assigned to user
    """
    company = crud.company.get(db=db, id=current_user.company_id)
    if company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already belongs to a company",
        )
    company = crud.company.create(db=db, obj_in=company_in)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred.",
        )
    crud.user.update_rank(db=db, db_obj=current_user, rank=RankEnum.GOVERNOR)
    company = crud.company.add_user(db=db, db_obj=company, user=current_user)
    return company


@router.put("/{id}", response_model=schemas.Company)
def update_company(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    company_in: schemas.CompanyUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update company
    """
    company = crud.company.get(db=db, id=id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company does not exist."
        )
    if current_user.company_id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have permissions for this company.",
        )
    if not current_user.rank or current_user.rank.value < RankEnum.GOVERNOR.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have rank of GOVERNOR.",
        )
    company = crud.company.update(db=db, db_obj=company, obj_in=company_in)
    return company


@router.delete("/{id}", response_model=schemas.Company)
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete company.
    """
    if not current_user.rank or current_user.rank.value < RankEnum.GOVERNOR.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must be GOVERNOR to delete company.",
        )
    company = crud.company.get(db=db, id=id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found."
        )
    if current_user.company_id != company.id:
        raise HTTPException(
            status_code=404, detail="User does not have access to that company."
        )
    company = crud.company.remove(db=db, id=id)
    return company


@router.post("/{company_id}/{user_id}/{rank}", response_model=List[schemas.User])
def add_user(
    *,
    db: Session = Depends(deps.get_db),
    company_id: uuid.UUID,
    user_id: uuid.UUID,
    rank: RankEnum,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Add user to company.
    """
    company = crud.company.get(db=db, id=company_id)
    user = crud.user.get(db=db, id=user_id)
    if not company or not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company or user not found."
        )
    if not current_user.rank or current_user.rank.value < RankEnum.CONSUL.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must be CONSUL or higher to add members",
        )
    if current_user.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to this company.",
        )
    company = crud.company.add_user(db=db, db_obj=company, user=current_user)
    user = crud.user.update(db=db, db_obj=user, obj_in={"rank": rank})
    return company.members
