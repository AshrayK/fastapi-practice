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
        orm_mode = True

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
    class Config: 
        orm_mode = True
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    owner : UserPostResponse

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
  
    created_at : datetime
    owner_id : int

    class Config:
        orm_mode = True

