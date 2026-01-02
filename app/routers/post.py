from fastapi import HTTPException,status,Depends,APIRouter
from typing import List
from .. import schemas,models,Oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc

router=APIRouter(prefix="/posts",tags=["Posts"])


@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(desc(models.Post.id)).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), get_current_user:int = Depends(Oauth2.get_current_user_id)):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found in db...")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):

    delete_query = db.query(models.Post).filter(models.Post.id == id)

    if not delete_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found in db...")

    delete_query.delete(synchronize_session=False)
    db.commit()
    return {}


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    query = db.query(models.Post).filter(models.Post.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found in db...")

    query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()
