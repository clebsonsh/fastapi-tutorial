from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    '/blog',
    tags=['Blog'],
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowBlog],
)
def index(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post(
    '/blog',
    tags=['Blog'],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowBlog,
)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        published=request.published,
        user_id=1
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get(
    '/blog/{id}',
    tags=['Blog'],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    return blog


@app.put(
    '/blog/{id}',
    tags=['Blog'],
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.ShowBlog,
)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )

    blog.update(request.dict())
    db.commit()

    return blog.first()


@app.delete(
    '/blog/{id}',
    tags=['Blog'],
    status_code=status.HTTP_204_NO_CONTENT,
)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )

    blog.delete(synchronize_session=False)
    db.commit()


@app.get(
    '/user',
    tags=['User'],
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowUser],
)
def index(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post(
    '/user',
    tags=['User'],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    '/user/{id}',
    tags=['User'],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowUser,
)
def show(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user
