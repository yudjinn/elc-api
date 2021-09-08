from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate
from app.models.company import Company
from app.core.config import settings


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    def create(self, db: Session, *, file: UploadFile, company: Company) -> File:
        # Save file to local storage
        compound_name = f"{company.name}_{file.filename}"
        try:
            with open(settings.FILE_STORAGE_ROUTE + compound_name) as output:
                output.write(file.file.read())
        except Exception as e:
            return e

        obj_in = File(
            file_name=file.filename, file_size=len(file.file), company=company
        )
        return super().create(db, obj_in)


file = CRUDFile(File)
