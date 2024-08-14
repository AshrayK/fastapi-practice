from typing import List
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/sqlalchemy",
    tags=["Posts"]
)
@router.get("/",response_model=List[schemas.PostResponse])
def root(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # new_posts=models.Posts(title=post.title, content=post.content, published=post.published)
    new_posts=models.Posts(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id:int, db:Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with user id: {id} was not found in the database.")
    
    return post
    
@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db:Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    
    if existing_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
    
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()

    db.refresh(existing_post)
    return post_query.first()


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    del_post = db.query(models.Posts).filter(models.Posts.id == id)
    if del_post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
    
    del_post.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


