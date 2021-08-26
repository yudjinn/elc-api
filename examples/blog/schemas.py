from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(User):
    blogs = List[Blog]

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    creator: ShowUser

    class Config:
        orm_mode = True
