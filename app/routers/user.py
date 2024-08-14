### CRUD USERS ###
from typing import List
from fastapi import Depends, HTTPException, status, APIRouter

from .. import models, schemas, utils
# from app import models, schemas, utils
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/",response_model=List[schemas.UserResponse])
def get_user(db: Session = Depends(get_db)):
    users=db.query(models.Users).all()
    return users

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(users:schemas.UserCreate,db:Session = Depends(get_db)):
    hashed_password = utils.hash(users.password)
    users.password = hashed_password

    new_user = models.Users(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User id : {id} was not found in the database.")
    
    return user

