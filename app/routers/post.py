from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])
credentials_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.get("/", response_model=List[schemas.ResponsePost])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )

    return posts


@router.post("/", response_model=schemas.ResponsePost)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    get_user=Depends(oauth2.get_user),
):
    new_post = models.Post(**post.dict(), user_id=get_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    return post


@router.put("/{id}", response_model=schemas.ResponsePost)
def update_post(
    id: int,
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    get_user: schemas.TokenData = Depends(oauth2.get_user),
):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    if post.user_id != get_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform the requested action",
        )

    query.update(**post.dict(), synchronize_session=False)
    db.commit()

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    get_user: schemas.TokenData = Depends(oauth2.get_user),
):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    if post.user_id != get_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to perform the requested action",
        )

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
