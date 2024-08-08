from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True

try:
    conn = psycopg.connect(
        host='localhost',
        dbname='fastapi',
        user='postgres',
        password='admin'
    )
    cursor = conn.cursor(row_factory=dict_row)

    print("Database connection was successful!")
    
except Exception as error:
    print("Connecting to database failed")
    print("Error:", error)
    time.sleep(2)

@app.get("/")
def root():
    return {"message":"Hello There!!"}

@app.get("/posts/")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data":posts}

@app.get("/posts/{id}")
def get_single_post(id:int):
    cursor.execute("""SELECT * FROM posts where id = (%s)""",(str(id),))
    get_single_post = cursor.fetchone()
    if not get_single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} not found.')
    return {"post":get_single_post}

@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title,post.content,post.published,str(id)))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
    return {"Updated Data": update_post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts where id = (%s) RETURNING * """,(str(id),))
    delete_single_post = cursor.fetchone()
    conn.commit()
    if delete_single_post  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')  
    return Response(status_code=status.HTTP_204_NO_CONTENT)




