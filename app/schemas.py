from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config: 
        # orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenDate(BaseModel):
    id: Optional[int]


class UserPostResponse(BaseModel):
    id : int
    email : EmailStr

        
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    # owner : UserPostResponse

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
  
    created_at : datetime
    owner_id : int
    owner: UserPostResponse

    class Config:
        # orm_mode = True
        from_attributes = True


class Vote(BaseModel):
    post_id : int
    dir : bool = False

class PostVote(BaseModel):
    Post : PostResponse
    votes : int

    class Config:
        # orm_mode = True
        from_attributes = True

class PostOut(BaseModel):
    Post : PostResponse
    votes : int

    class Config:
        from_attributes = True
