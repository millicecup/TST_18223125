from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: schemas.PostCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    # optional: cek channel
    channel = db.query(models.Channel).get(payload.channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Channel not found")

    post = models.Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/", response_model=list[schemas.PostRead])
def list_posts(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return db.query(models.Post).all()
