from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
import uuid

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.models.bank import Bank
from app.models.company import Company
from app.models.user import User
from app.utils import StatusEnum, RankEnum


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_all_by_bank(self, db: Session, *, bank: Bank) -> List[Transaction]:
        return db.query(Transaction).where(bank_id=bank.id).all()

    def get_multi_by_company(
        self, db: Session, *, company: Company, skip: int, limit: int
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .join(Transaction.bank)
            .where(company_id=company.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_by_bank_scoped(
        self, db: Session, *, bank: Bank, scope: StatusEnum
    ) -> List[Transaction]:
        return db.query(Transaction).where(bank_id=bank.id).where(status=scope).all()

    def get_multi_by_company_scoped(
        self, db: Session, *, company: Company, scope: StatusEnum, skip: int, limit: int
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .join(Transaction.bank)
            .where(company_id=company.id)
            .where(status=scope)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self, db: Session, *, obj_in: TransactionCreate, creator: User
    ) -> Transaction:
        db_item = Bank(**obj_in.dict(), creator_id=creator.id)
        return super().create(db, obj_in=db_item)

    def update(
        self,
        db: Session,
        *,
        db_obj: Transaction,
        obj_in: Union[Transaction, Dict[str, Any]],
    ) -> Transaction:
        if db_obj.status is not StatusEnum.PENDING:
            # Error
            pass
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def approve(
        self, db: Session, *, db_obj: Transaction, obj_in: Transaction, approver: User
    ) -> Transaction:
        if approver.rank < RankEnum.CONSUL:
            # Error, not enough rank
            pass
        update_data = obj_in.dict()
        update_data["status"] = StatusEnum.APPROVED
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, id: uuid.UUID) -> Transaction:
        db_obj = db.query(Transaction).get(id)
        if db_obj.status is StatusEnum.APPROVED:
            # Error, already approved cannot remove
            pass
        return super().remove(db, id=id)


transaction = CRUDTransaction(Transaction)
