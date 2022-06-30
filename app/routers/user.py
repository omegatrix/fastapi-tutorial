from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..utils import generate_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.ResponseUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get("/{id}", response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )

    return user


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    pwd_hash = generate_hash(user.password)
    user.password = pwd_hash
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
