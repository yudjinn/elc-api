from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from . import schemas, models, database
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=request.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", response_model=schemas.ShowBlog)
def get_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return blog


@app.post("/user")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        username=request.username, email=request.email, password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/user/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
