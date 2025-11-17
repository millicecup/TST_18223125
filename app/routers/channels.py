from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/channels", tags=["channels"])


@router.post("/", response_model=schemas.ChannelRead)
def create_channel(payload: schemas.ChannelCreate, db: Session = Depends(get_db)):
    channel = models.Channel(**payload.dict())
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


@router.get("/", response_model=list[schemas.ChannelRead])
def list_channels(db: Session = Depends(get_db)):
    return db.query(models.Channel).all()
