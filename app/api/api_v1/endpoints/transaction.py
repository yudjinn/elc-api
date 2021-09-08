from backend.app.utils import StatusEnum
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app import crud, models, schemas
from app.api import deps
from app.utils import RankEnum

router = APIRouter()


@router.get("/", response_model=List[schemas.Transaction])
def get_multi_approved(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    *skip: int,
    limit: int,
) -> Any:
    """
    Return approved transactions for company (spanning banks)
    """
    if not current_user.company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not have a company"
        )
    transactions = crud.transaction.get_multi_by_company_scoped(
        db=db,
        company=current_user.company,
        scope=StatusEnum.APPROVED,
        skip=skip,
        limit=limit,
    )
    return transactions


@router.get("/{scope}", response_model=List[schemas.Transaction])
def get_multi_pending(
    scope: StatusEnum,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    *skip: int,
    limit: int,
) -> Any:
    """
    Return pending transactions for company (spanning banks)
    """
    if not current_user.company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not have a company"
        )
    transactions = crud.transaction.get_multi_by_company_scoped(
        db=db,
        company=current_user.company,
        scope=scope,
        skip=skip,
        limit=limit,
    )
    return transactions


@router.get("/{bank_id}", response_model=List[schemas.Transaction])
def get_all_by_bank(
    bank_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    bank = crud.bank.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank ID does not exist"
        )
    if bank.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to that bank.",
        )
    transactions = crud.transaction.get_all_by_bank_scoped(
        db=db, bank=bank, scope=StatusEnum.APPROVED
    )
    return transactions


@router.get("/{bank_id}/{scope}", response_model=List[schemas.Transaction])
def get_all_by_bank(
    bank_id: uuid.UUID,
    scope: StatusEnum,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    bank = crud.bank.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank ID does not exist"
        )
    if bank.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to that bank.",
        )
    transactions = crud.transaction.get_all_by_bank_scoped(
        db=db, bank=bank, scope=scope
    )
    return transactions


@router.get("/{id}", response_model=schemas.Transaction)
def get_transaction(
    id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction does not exist"
        )
    if current_user.company_id != transaction.bank.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to that company's transactions.",
        )
    return transaction
