from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


@router.post("/", response_model=schemas.DashboardRead, status_code=status.HTTP_201_CREATED)
def create_dashboard(
    payload: schemas.DashboardCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    dashboard = models.Dashboard(**payload.model_dump())
    db.add(dashboard)
    db.commit()
    db.refresh(dashboard)
    return dashboard


@router.get("/", response_model=list[schemas.DashboardRead])
def list_dashboards(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return db.query(models.Dashboard).all()
