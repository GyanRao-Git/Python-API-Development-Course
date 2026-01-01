from pydantic_settings import BaseSettings
from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()



try:
    conn = psycopg2.connect(
        host=settings.DB_HOST, database=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD,cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("DB connection was succesfull..")
except Exception as error:
    print("Connection to db failed...")
    print("Error: ",error)
    time.sleep(2)

class Post(BaseModel):
    title:str
    content:str
    published:bool


@app.get('/posts')
async def get_posts():
    posts=cursor.execute("""Select * from posts order by id""")
    posts=cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):
    cursor.execute(""" INSERT into posts (title,content,published) values(%s ,%s ,%s) returning * """,(post.title,post.content,post.published)) 
    new_post=cursor.fetchone() 
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
async def get_post(id:int):
    cursor.execute(""" Select * from posts where id = %s""",(str(id)))

    post=cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found in db...")

    return {"data":post}


@app.delete("/posts/{id}",status_code=status.HTTP_200_OK)
async def delete_post(id:int):
    cursor.execute("""delete from posts where id=%s returning * """,(str(id)))
    conn.commit()
    deleted_post=cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found in db...")
    return {"data":deleted_post}


@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
async def update_post(id:int , post:Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s returning *""",(post.title,post.content,post.published,str(id)))
    updated_post= cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found in db...")
    return {"data":updated_post}
    


 