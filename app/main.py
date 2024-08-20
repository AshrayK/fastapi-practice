from .database import Base, engine, get_db
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote

from fastapi.middleware.cors import CORSMiddleware

### This is causing error as models is getting overwritten for some reason
# models = Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [

    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

### CRUD POSTS ###
@app.get("/")   
def root(db: Session = Depends(get_db)):
    return {"message":"done"}
