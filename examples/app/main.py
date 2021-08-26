from fastapi import Depends, FastAPI, status

from .dependencies import get_query_token, get_token_header
from .routers import users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
