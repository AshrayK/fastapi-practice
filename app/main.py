from typing import List
from . import models, schemas
from .models import Posts, Users
from .database import Base, engine, get_db
from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from psycopg.rows import dict_row
import time
import psycopg


### This is causing error as models is getting overwritten for some reason
# models = Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

### CRUD POSTS ###
@app.get("/")   
def root(db: Session = Depends(get_db)):
    return {"message":"done"}

@app.get("/sqlalchemy",response_model=List[schemas.PostResponse])
def root(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


@app.post("/sqlalchemy",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # new_posts=models.Posts(title=post.title, content=post.content, published=post.published)
    new_posts=models.Posts(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@app.get("/sqlalchemy/{id}",response_model=schemas.PostResponse)
def get_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with user id: {id} was not found in the database.")
    
    return post
    
@app.put("/sqlalchemy/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    
    if existing_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
    
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()

    db.refresh(existing_post)
    return post_query.first()


@app.delete("/sqlalchemy/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):
    del_post = db.query(models.Posts).filter(models.Posts.id == id)
    if del_post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
    
    del_post.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

### CRUD USERS ###
@app.get("/users",response_model=List[schemas.UserResponse])
def get_user(db: Session = Depends(get_db)):
    users=db.query(models.Users).all()
    return users

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(users:schemas.UserCreate,db:Session = Depends(get_db)):
    new_user = models.Users(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


