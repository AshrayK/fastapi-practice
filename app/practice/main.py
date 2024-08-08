from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message":"Hello world"}

@app.get("/home/")
async def root():
    return {"Key":"value"}

myposts = [{
    "title":"This is the new post1",
    "content" : "this is the new content",
    "published" : True,
    "rating" : 5,
    "id":1},
    {
    "title":"This is the new post2",
    "content" : "this is the new content2",
    "published" : True,
    "rating" : 4,
    "id":2
    }
]

def findposts(id):
    return next((post for post in myposts if post["id"]==id),None)

# def find_posts(id):
#     return next(filter(lambda post: post["id"] == id, myposts), None)

@app.get("/posts/")
async def posts():
    return {"message":myposts}

@app.post("/posts/")
async def create_posts(post:Post,status_code =status.HTTP_201_CREATED):
    post_dict = post.dict()
    post_dict["id"]=randrange(0,10000)
    myposts.append(post_dict)
    return {"message":post_dict} 

@app.get("/posts/latest/")
async def getpost():
    post = myposts[len(myposts)-1]
    return {"Details":post}

@app.get("/posts/{id}/")
async def getgpost(id: int,response : Response):
    post = findposts(int(id))
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data with id:{id} Not Found.")
    print(post)
    return {"Details":post}

@app.post("/creatingpost/")
async def creatingpost(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": f'We have created a title: {payLoad["title"]}=> content: {payLoad["content"]}'}

@app.post("/gettingpost/")
async def gettingpost(getpost: Post):
    print(getpost)
    print(getpost.title)
    print(getpost.published)
    print(getpost.rating)
    return {"message":getpost}

def delete_post(id):
    for i , p in enumerate(myposts):
        if p["id"] == id:
            return i

# def delete_post(id):
#     try:
#         return myposts.index(next(p for p in myposts if p["id"] == id))
#     except StopIteration:
#         return None

@app.delete("/posts/{id}/")
def deletepost(id: int,status_code = status.HTTP_204_NO_CONTENT):
    index = delete_post(id)
    if index is None:
        raise HTTPException(status_code=404, detail="Post not found")
    myposts.pop(index)
    # return {"message": "Post has been removed."}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def find_index_post(id):
    for i, p in enumerate(myposts):
        if p["id"] == id:
            return i

@app.put("/posts/{id}/")
def updatepost(id: int, post: Post):
    index = find_index_post(id)
    if index is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail =f'posts with id: {id} does not exist.')
    post_dict = post.dict()
    post_dict["id"] = id
    myposts[index]=post_dict
    return {"Data":post_dict}