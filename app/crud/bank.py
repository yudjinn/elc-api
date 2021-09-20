from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
import uuid

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.bank import Bank
from app.schemas.bank import BankCreate, BankUpdate
from app.models.company import Company
from app.models.user import User


class CRUDBank(CRUDBase[Bank, BankCreate, BankUpdate]):
    def get_all_by_company(self, db: Session, *, company: Company) -> List[Bank]:
        company = db.query(Company).filter(Company.id == company.id).first()
        return company.banks

    def create(self, db: Session, *, obj_in: BankCreate, company_id: uuid.UUID) -> Bank:
        db_item = Bank(**obj_in.dict(), company_id=company_id)
        return super().create(db, obj_in=db_item)

    def update(
        self, db: Session, *, db_obj: Bank, obj_in: Union[BankUpdate, Dict[str, Any]]
    ) -> Bank:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


bank = CRUDBank(Bank)
