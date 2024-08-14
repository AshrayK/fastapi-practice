from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import database, models, schemas, utils, oauth2
from sqlalchemy.orm import Session

router= APIRouter(
    tags=["Authentication"]
)


@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid username or password.")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid username or password.")
    
    access_token = oauth2.create_token(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/login")
# def login(user_credentials: schemas.UserLogin,db: Session = Depends(database.get_db)):

#     user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Invalid username or password.")
    
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                             detail=f'Invalid username or password.')

#     access_token = oauth2.create_token(data = {"user_id":user.id})

#     return {"access_token" : access_token , "token_type": "bearer"}

