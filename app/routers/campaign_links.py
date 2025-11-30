from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..routers.auth import get_current_user

router = APIRouter(prefix="/campaign-links", tags=["campaign_links"])

@router.post("/", response_model=schemas.CampaignLinkRead)
def create_link(payload: schemas.CampaignLinkCreate,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    link = models.CampaignLink(**payload.model_dump())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.get("/", response_model=list[schemas.CampaignLinkRead])
def list_links(db: Session = Depends(get_db),
               user=Depends(get_current_user)):
    return db.query(models.CampaignLink).all()
