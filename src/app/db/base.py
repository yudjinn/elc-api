# Import all the models so init_db has them

from app.models.base import Base  # noqa
from app.models.bank import Bank  # noqa
from app.models.company import Company  # noqa
from app.models.file import File  # noqa
from app.models.transaction import Transaction  # noqa
from app.models.user import User  # noqa
