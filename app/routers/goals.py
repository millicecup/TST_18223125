from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/", response_model=schemas.GoalRead, status_code=status.HTTP_201_CREATED)
def create_goal(
    payload: schemas.GoalCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    campaign = db.query(models.Campaign).get(payload.campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campaign not found")

    goal = models.Goal(**payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("/", response_model=list[schemas.GoalRead])
def list_goals(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return db.query(models.Goal).all()
