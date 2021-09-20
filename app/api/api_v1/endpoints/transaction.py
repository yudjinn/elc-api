from app.utils import StatusEnum
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


@router.post("/{bank_id}", response_model=schemas.Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    bank_id: uuid.UUID,
    transaction_in: schemas.TransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new transaction for bank
    """
    bank = crud.bank.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank does not exist"
        )
    if current_user.company_id != bank.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not belong to that bank's company.",
        )
    transaction = crud.transaction.create(
        db=db, obj_in=transaction_in, creator=current_user
    )
    return transaction


@router.put("/{id}", response_model=schemas.Transaction)
def update_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    transaction_in: schemas.TransactionUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update Transaction
    """
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction does not exist."
        )
    bank = crud.bank.get(db=db, id=transaction.bank_id)
    if current_user.company_id != bank.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to that company's transactions.",
        )
    if (
        current_user.rank.value < RankEnum.CONSUL.value
        or current_user.id != transaction.creator_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have permissions for this transaction.",
        )
    # dont allow user to change status, only approve endpoints do that
    transaction_in.status = transaction.status
    transaction = crud.transaction.update(
        db=db, db_obj=transaction, obj_in=transaction_in
    )
    return transaction


@router.put("/{id}/approve", response_model=schemas.Transaction)
def approve_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction does not exist."
        )
    if current_user.company_id != transaction.bank.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to that company's transactions.",
        )
    if current_user.rank.value < RankEnum.CONSUL.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be CONSUL or greater to approve.",
        )
    transaction = crud.transaction.approve(
        db=db, db_obj=transaction, approver=current_user
    )
    return transaction


@router.delete("/{id}", response_model=schemas.Transaction)
def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction does not exist."
        )
    if transaction.status is StatusEnum.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction is approved, cannot be deleted.",
        )
    if current_user.company_id != transaction.bank.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have access to that company's transactions.",
        )
    if (
        current_user.rank.value < RankEnum.CONSUL.value
        or transaction.creator_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be CONSUL or greater to approve.",
        )
