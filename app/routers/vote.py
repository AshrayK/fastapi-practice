from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from ..database import get_db

router = APIRouter(
    prefix ="/vote",
    tags =["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def root(vote : schemas.Vote,db: Session = Depends(get_db), user_current: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f'Post with id: {vote.post_id} was not found.')


    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user_current.id)
    found_vote = vote_query.first()

    if (vote.dir == True):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                detail =f" User id: {user_current.id} has already voted for the post : {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = user_current.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Updated Vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail =f" User id: {user_current.id} has already voted for the post : {vote.post_id}")
        
        vote_query.delete(synchronize_session=False)
        db.commit() 
        return {"message":"Deleted Vote"}
