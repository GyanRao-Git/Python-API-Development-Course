from fastapi import HTTPException, status, Depends, APIRouter
from .. import schemas, models,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users available")

    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with id: {id} does not exist...")

    return user


