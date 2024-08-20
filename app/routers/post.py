from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from app.database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/sqlalchemy",
    tags=["Posts"]
)

# @router.get("/")
# def root(db: Session = Depends(get_db), user_current: int = Depends(oauth2.get_current_user),
#          limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
#     # Query posts with optional title search and pagination
#     query = db.query(models.Posts, func.count(models.Votes.post_id).label("Votes")).join(
#         models.Votes, models.Votes.post_id == models.Posts.id, isouter=True
#     ).filter(models.Posts.title.contains(search)).group_by(models.Posts.id).limit(limit).offset(skip)
    
#     results = query.all()

#     # Serialize the results
#     serialized_results = []
#     for post, vote_count in results:
#         post_dict = post.__dict__.copy()  # Convert SQLAlchemy object to dictionary
#         post_dict["Votes"] = vote_count   # Add the vote count to the dictionary
#         post_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state
#         serialized_results.append(post_dict)

#     return serialized_results

@router.get("/",response_model=List[schemas.PostResponse])
def root(db: Session = Depends(get_db), user_current: int = Depends(oauth2.get_current_user),
         limit : int = 10, skip : int = 0
         ,search : Optional[str] = ""):
    # print(user_current.id)
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip)

    ## for only the user to get only his posts
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == user_current.id).all()

    return posts



# @router.get("/customVotes/",response_model = List[schemas.PostOut])
# def custom(db: Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
#     results = db.query(models.Posts, func.count(models.Votes.post_id)
#                        .label("Votes")).join(models.Votes, 
#                                              models.Posts.id == models.Votes.post_id, 
#                                              isouter =True).group_by(models.Posts.id).all()
#     return results

@router.get("/customVotes/", response_model=List[schemas.PostOut])
def custom(db: Session = Depends(get_db), user_current: int = Depends(oauth2.get_current_user)):
    results = db.query(
        models.Posts,
        func.count(models.Votes.post_id).label("votes")
    ).join(
        models.Votes,
        models.Posts.id == models.Votes.post_id,
        isouter=True
    ).group_by(
        models.Posts.id
    ).all()
    
    # Transform the result to match the response model structure
    response_data = [
        {"Post": post, "votes": votes}
        for post, votes in results
    ]
    
    return response_data

 
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),user_current: int = Depends(oauth2.get_current_user)):
    
    # new_posts=models.Posts(title=post.title, content=post.content, published=post.published)
    new_posts=models.Posts(**post.dict(),owner_id=user_current.id)
    print(user_current.id)
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id:int, db:Session = Depends(get_db),user_current: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with user id: {id} was not found in the database.")
    
    ## if you want only yourself to view only ur posts
    # if post.owner_id != user_current.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
    #                         detail = f'User id: {id} is not authorized to perform this action on the post.')
    
    return post
    
@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db:Session = Depends(get_db),user_current: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    
    if existing_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
    
    if existing_post.owner_id != user_current.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f'User id: {id} is not authorized to perform this action.')
    
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()

    db.refresh(existing_post)
    return post_query.first()


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db),user_current: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    del_post = post_query.first()

    if del_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')

    if del_post.owner_id != user_current.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = f'User id: {id} is not authorized to perform this action on the post.')
    
    post_query.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


