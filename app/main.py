from fastapi import FastAPI,status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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


@app.get('/sqlalchemy')
async def test_posts(db:Session=Depends(get_db)):
    posts= db.query(models.Post).all()
    return {"data":posts}


@app.get('/posts')
async def get_posts(db: Session = Depends(get_db)):
    # posts=cursor.execute("""Select * from posts order by id""")
    # posts=cursor.fetchall()
    posts = db.query(models.Post).order_by(desc(models.Post.id)).all()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT into posts (title,content,published) values(%s ,%s ,%s) returning * """,(post.title,post.content,post.published)) 
    # new_post=cursor.fetchone() 
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" Select * from posts where id = %s""",(str(id)))
    # post=cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found in db...")

    return {"data":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""delete from posts where id=%s returning * """,(str(id)))
    # conn.commit()
    # deleted_post=cursor.fetchone()
    delete_query=db.query(models.Post).filter(models.Post.id==id)

    if not delete_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found in db...")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return {}


@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post= cursor.fetchone()
    # conn.commit()

    query=db.query(models.Post).filter(models.Post.id==id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found in db...")
    
    query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return {"data":query.first()}
    


 